import numpy as np
import json
import time
import math
from collections import defaultdict
import scipy.io
# from scipy.integrate import RK45, solve_ivp


from . import base
from . import units

mL = units.ureg("mL")
mmHg = units.ureg("mmHg")
s = units.ureg("s")


class Zenkur(base.CirculationModel):
    """
    0D model of the left ventricle only.

    """

    def __init__(self, parameters: dict[str, float] | None = None, add_units=False):
        super().__init__(parameters, add_units=add_units)

        fluidVolume = 1000  # % resuscitation volume

        self.startTime = 600
        self.endTime = 1600
        self.startTimeRes = 2000
        self.endTimeRes = 3000
        self.totalVolume = fluidVolume

        # total experiment time
        self.tspan = [0, 3600]  # % 60 minutes

        # resolution
        self.resolution = 10000

        # %% parameters, finalized for paper...
        self.apSetpoint = 70  # % setpoint for baroreflex regulation of mean arterial pressure; % setpoint for baroreflex regulation of mean arterial pressure
        self.satSna = 25  # % deviation from setpoint in mmHg where SNA reaches 99% saturation either way; % deviation from setpoint in mmHg where SNA reaches 99% saturation either way
        self.Ca = 4  # % arterial compliance, Ursino 1994; % arterial compliance
        self.VaUnstressed = 700  # % unstressed arterial volume; % venous compliance
        self.Va_relaxed = self.VaUnstressed  # % unstressed arterial volume
        self.minVvUnstressed = 2700
        self.maxVvUnstressed = 3100
        self.minVv_relaxed = self.minVvUnstressed  # % and venous (controlled)
        self.maxVv_relaxed = self.maxVvUnstressed
        self.Cv = 111.11  # % Ursino 1994

        self.hrMin = 40 / 60  # % minimum heart rate
        self.hrMax = 180 / 60  # % maximum heart rate

        self.Tsyst = (
            1 / self.hrMax * 0.8
        )  # % duration of systole, constant for now such that systole takes 80% of cycle at max heart rate, Friedberg 2006 fig. 4A; % duration of systole, constant for now
        self.RartMin = (
            0.5 * 1.067
        )  # % minimal arterial resistance (at 0 SNA); %relative to Ursino, 1994; % minimal arterial resistance (at 0 SNA)
        self.RartMax = (
            2 * 1.067
        )  # % maximal arterial resistance (at 1 SNA); % maximal arterial resistance (at 1 SNA)
        self.Rvalve = 2.5e-3  # % resistance "tricuspid" valve, from Ursino, 1998; % resistance "tricuspid" valve

        # % use fitting results for diastolic compliance pars
        fitResults = scipy.io.loadmat("opt_p0lv_kelv_v0lv_glower_control.mat")
        self.P0lv = fitResults["P0lv"][0][0]
        self.kelv = fitResults[
            "kelv"
        ][
            0
        ][
            0
        ]  # % ventricular relaxation constant; % scaling constant for ventricular relaxation
        self.Vlved0 = fitResults["V0lv"][0][0]  # % unstressed volume LV

        self.cfactor = 1  # % multiply contractility response range by this...

        self.contractilityMin = (
            self.cfactor * 0.5 * 69 / 1.33
        )  # % half of mean from global study in Glower, 1985
        self.contractilityMax = self.cfactor * 2 * 69 / 1.33  # % and twice the mean
        self.lowPassCutoff = 0.008  # % cutoff of peripheral effector lowpass, using time constant for unstressed venous volume from Ursino, 1998

        self.fixedSNA = -1  # % closed loop; % if < 0, baroreflex feedback loop closed, otherwise SNA fixed to that level

        # %% end model parameters

        # %% initial conditions etc.
        totalVolume = 4825

        # % split by unstressed volumes for intial guess
        meanVvU = (self.minVvUnstressed + self.maxVvUnstressed) / 2
        Va = totalVolume / (self.VaUnstressed + meanVvU) * self.VaUnstressed
        Vv = totalVolume / (self.VaUnstressed + meanVvU) * meanVvU
        self.y = [
            Va,
            Vv,
            0.5,
            3 * self.Vlved0,
            2 * self.Vlved0,
        ]  # % start with midpoint sna, really rough guesses for Vlvs

        ############ Chambers
        chambers = self.parameters["chambers"]

        self.E_LV = self.time_varying_elastance(**chambers["LV"])
        self.p_LV_func = lambda V, t: self.E_LV(t) * (V - chambers["LV"]["V0"])
        self.var = {}
        self.results = defaultdict(list)

    @staticmethod
    def default_parameters() -> base.CirculcationModelParams:
        return {
            "BPM": 75.0 * units.ureg("1/minutes"),
            "chambers": {
                "LV": {
                    "EA": 2.75 * mmHg / mL,
                    "EB": 0.008 * mmHg / mL,
                    "TC": 0.34 * s,
                    "TR": 0.17 * s,
                    "tC": 0.00 * s,
                    "V0": -9.0 * mL,
                },
            },
            "circulation": {
                "SYS": {
                    "Rao": 0.5 * mmHg * s / mL,
                    "R_sys": 2.5 * mmHg * s / mL,
                    "p_dia": 10.0 * mmHg,
                    "C_sys": 0.1 * mL / mmHg,
                    "Pp": 4.5 * mmHg,
                },
            },
        }

    @staticmethod
    def default_initial_conditions() -> dict[str, float]:
        return {
            "V_LV": 100.0 * mL,
            "p_ao": 70.0 * mmHg,
            "dp_ao_dt": 0.0 * mmHg / s,
        }

    def Pa(self, Va, Ca, Va_relaxed):
        # % calculate arterial pressure
        return (Va - Va_relaxed) / Ca  # pressure

    def Pv(self, Vv, Cv, Vv_relaxed):
        return (Vv - Vv_relaxed) / Cv  # pressure

    def PvComplete(self, Vv, Cv, minVv_relaxed, maxVv_relaxed, snaEffector):
        return (
            Vv - ((maxVv_relaxed - minVv_relaxed) * (1 - snaEffector) + minVv_relaxed)
        ) / Cv  # pressure

    def calcSna(self, delayedAp, apSetpoint, satSna):
        # % calculate sympathetic nervous activity from arterial pressure, satSna
        # % determines 99% saturation point
        return 1 - (
            1 / (1 + np.exp(-4.595119850 * (delayedAp - apSetpoint) / satSna))
        )  # sna

    def vlves(self, C, Vlved, Vlved0, Pej, P0lv, kelv):
        # """calculate endsystolic volume as a function of a lot of other things...

        denom = Pej - P0lv * (
            np.exp(kelv * (Vlved - Vlved0)) - 1
        )  # % pressure difference between large arteries and ventricle at end-diastole

        # if denom > 0: # art. pressure > Plved, work to perform
        #     # JTG: max([a b])    concatenate((a,b)).max()    max of all values in two vectors
        #     #return np.max([Vlved0, Vlved-C*(Vlved-Vlved0)/denom]) # Vlves

        #     return np.concatenate(([Vlved0], [Vlved-C*(Vlved-Vlved0)/denom])).max()
        # else: # no work, maximally contract
        #     return Vlved0 # Vlves

        _ = np.where(denom > 0, Vlved - C * (Vlved - Vlved0) / denom, Vlved0)
        return np.where(denom > _, Vlved0, _)

    def vlved(self, t_ed, Pcvp, kelv, P0lv, Rvalve, Ves, Vlved0):
        # """calculate enddiastolic volume as a function of a lot of other things...

        # JTG: essentially test if blood coming from central venous pressure is greater mmHg than ventricle at end of systole -- P_CVP > P_ES, ref eq.'s 39 + 29 Curcio
        deltap = Pcvp + P0lv * (
            1 - np.exp(kelv * (Ves - Vlved0))
        )  # % pressure difference between central veins and ventricle drives filling

        # JTG: Old logic doesn't translate well --
        # if deltap > 0:
        #     k1 = -P0lv / Rvalve * np.exp(-kelv * Vlved0)
        #     k2 = kelv
        #     k3 = (Pcvp + P0lv)/Rvalve

        #     # JTG: may need alot of floating point work here
        #     return -1 / k2 * np.log(k1 / k3 * (np.exp(-k2 * k3 * t_ed)-1)+np.exp(-k2*(Ves+k3 * t_ed))) # % solution of ODE, see paper; Vlved
        # else:
        #     return Ves # % can't fill => ventricular volume remains at current endsystolic volume

        return np.where(
            deltap > 0,
            (
                -1
                / kelv
                * np.log(
                    (-P0lv / Rvalve * np.exp(-kelv * Vlved0))
                    / ((Pcvp + P0lv) / Rvalve)
                    * (np.exp(-kelv * ((Pcvp + P0lv) / Rvalve) * t_ed) - 1)
                    + np.exp(-kelv * (Ves + ((Pcvp + P0lv) / Rvalve) * t_ed))
                )
            ),
            Ves,
        )

    def update_static_variables(self, t):
        self.var["p_LV"] = self.p_LV_func(self.state["V_LV"], t)

    def volumeChange(
        self, t, startTime, endTime, startTimeRes, endTimeRes, totalVolume
    ):
        # % input function for model to simulate fluid resuscitation/withdrawal
        if t >= startTime and t < endTime:
            return -totalVolume / (endTime - startTime)  # dVdt
        elif t >= startTimeRes and t < endTimeRes:
            return totalVolume / (endTimeRes - startTimeRes)  # dVdt
        else:
            return 0  # dVdt

    def step(self, t, dt):
        # self.update_static_variables(t)

        # % states
        Va = self.y[0]  # % volume in arterial compartment
        PaDel = self.Pa(
            self.y[0], self.Ca, self.Va_relaxed
        )  # % arterial pressure, delayed by sna delay (from delayed Va)
        Vv = self.y[1]  # % volume in venous compartment

        if self.fixedSNA < 0:  # % closed loop
            snaEffector = self.y[2]  # % low-pass filtered peripheral response to SNA
        else:
            # %%%%%%% open reflex
            snaEffector = self.fixedSNA

        # %%% our ventricular filling states
        Vlved = self.y[3]  # % enddiastolic volume
        Vlves = self.y[4]  # % endsystolic volume, difference gives stroke volume...

        # % baroreflex nonlinearity
        sna = self.calcSna(PaDel, self.apSetpoint, self.satSna)
        # % simple low-pass filter
        if self.fixedSNA < 0:  # % loop closed
            dSnaEffector = (
                2 * math.pi * self.lowPassCutoff * (sna - snaEffector)
            )  # % first order low-pass
        # %%% open reflex
        else:
            dSnaEffector = 0

        hr = (self.hrMax - self.hrMin) * snaEffector + self.hrMin

        Rart = (self.RartMax - self.RartMin) * snaEffector + self.RartMin
        C = (
            self.contractilityMax - self.contractilityMin
        ) * snaEffector + self.contractilityMin

        Vv_relaxed = (self.maxVv_relaxed - self.minVv_relaxed) * (
            1 - snaEffector
        ) + self.minVv_relaxed

        Pa1 = self.Pa(Va, self.Ca, self.Va_relaxed)
        Pv1 = self.Pv(Vv, self.Cv, Vv_relaxed)

        Rtpr = Rart  # % extremely primitive, no venoles or anything
        Ic = (Pa1 - Pv1) / Rtpr  # % total flow through capillary streambed

        t_ed = 1 / hr - self.Tsyst  # % duration of diastole, endpoint of filling

        Ico = (Vlved - Vlves) * hr  # % cardiac output is stroke volume * heart rate

        # dVa
        dVa = Ico - Ic

        # % now calculate next step of discrete iteration at current point
        nextVlves = self.vlves(C, Vlved, self.Vlved0, Pa1, self.P0lv, self.kelv)
        nextVlved = self.vlved(
            t_ed, Pv1, self.kelv, self.P0lv, self.Rvalve, Vlves, self.Vlved0
        )

        # dVlves and dVlved
        # % rates of change are average rates of change of discrete dynamical system over a whole beat in current situation
        dVlves = (nextVlves - Vlves) * hr
        dVlved = (nextVlved - Vlved) * hr

        # dVv
        dVv = -dVa + self.volumeChange(
            t,
            self.startTime,
            self.endTime,
            self.startTimeRes,
            self.endTimeRes,
            self.totalVolume,
        )  # % external volume substitution/withdrawal affects venous compartment

        self.y[0] += dt * dVa
        self.y[1] += dt * dVv
        self.y[2] += dt * dSnaEffector
        self.y[3] += dt * dVlved
        self.y[4] += dt * dVlves

        self.results["time"].append(t)
        self.results["V_LV"].append(self.y[1])
        self.results["p_LV"].append(Pv1)

        # return [dVa, dVv, dSnaEffector, dVlved, dVlves]

    def print_info(self):
        C_VEN_SYS = self.parameters["circulation"]["SYS"]["C_VEN"]
        C_AR_SYS = self.parameters["circulation"]["SYS"]["C_AR"]

        print("V_LV      = %4.2f mL" % self.state["V_LV"])
        print("V_AR_SYS  = %4.2f mL" % (C_AR_SYS * self.state["p_AR_SYS"]))
        print("V_VEN_SYS = %4.2f mL" % (C_VEN_SYS * self.state["p_VEN_SYS"]))

        V_tot_heart = (
            self.state["V_LA"]
            + self.state["V_LV"]
            + self.state["V_RA"]
            + self.state["V_RV"]
        )
        V_tot_SYS = (
            C_AR_SYS * self.state["p_AR_SYS"] + C_VEN_SYS * self.state["p_VEN_SYS"]
        )

        V_tot = V_tot_heart + V_tot_SYS
        print("======================")
        print("V (heart) = %4.2f mL" % V_tot_heart)
        print("V (SYS)   = %4.2f mL" % V_tot_SYS)
        print("======================")
        print("V         = %4.2f mL" % V_tot)
