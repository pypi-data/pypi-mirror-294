import numpy as np
import json
import time
from collections import defaultdict
# from scipy.integrate import RK45, solve_ivp


from . import base
from . import units

mL = units.ureg("mL")
mmHg = units.ureg("mmHg")
s = units.ureg("s")


class LVOnly(base.CirculationModel):
    """
    0D model of the left ventricle only.

    """

    def __init__(self, parameters: dict[str, float] | None = None, add_units=False):
        super().__init__(parameters, add_units=add_units)

        ############ Chambers
        chambers = self.parameters["chambers"]

        self.E_LV = self.time_varying_elastance(**chambers["LV"])

        ############ Valves
        # valves = self.parameters["valves"]

        # if self._add_units:
        #     unit_R = 1 * mmHg * s / mL
        #     unit_p = 1 * mmHg
        # else:
        #     unit_R = 1
        #     unit_p = 1

        # self.R_AV = self._R(
        #     valves["AV"]["Rmin"], valves["AV"]["Rmax"], unit_R=unit_R, unit_p=unit_p
        # )
        # self.R_MV = self._R(
        #     valves["MV"]["Rmin"], valves["MV"]["Rmax"], unit_R=unit_R, unit_p=unit_p
        # )

        ############ PV relationships
        self.p_LV_func = lambda V, t: self.E_LV(t) * (V - chambers["LV"]["V0"])
        self.var = {}

    @staticmethod
    def default_parameters() -> base.CirculcationModelParams:
        return {
            "BPM": 75.0 * units.ureg("1/minutes"),
            "chambers": {
                "LV": {
                    "EA": 2.75 * mmHg / mL,
                    "EB": 0.08 * mmHg / mL,
                    "TC": 0.34 * s,
                    "TR": 0.17 * s,
                    "tC": 0.00 * s,
                    "V0": 5.0 * mL,
                },
            },
            "circulation": {
                "SYS": {
                    "Rao": 0.5 * mmHg * s / mL,
                    # "Pao": 52.5 * mmHg,
                    "Rp": 2.5 * mmHg * s / mL,
                    "EDP": 10.0 * mmHg,
                    "Cao": 0.1 * mL / mmHg,
                    "Pp": 4.5 * mmHg,
                    # "aortic_resistance": 0.5,
                    # "systematic_resistance": 2.5,
                    # "systematic_compliance": 0.1,
                    # "aortic_pressure": 10,
                    # "diastolic_pressure": 10,
                    # "initial_pressure": 0.0,
                },
            },
        }

    @staticmethod
    def default_initial_conditions() -> dict[str, float]:
        return {
            "V_LV": 120.0 * mL,
            "P_ao": 10.0 * mmHg,
            "dp_ao_dt": 0.0 * mmHg / s,
            # "Q_AR_SYS": 0.0 * mL / s,
            # "Q_VEN_SYS": 0.0 * mL / s,
        }

    def update_static_variables(self, t):
        self.var["p_LV"] = self.p_LV_func(self.state["V_LV"], t)

        Pao = self.parameters["circulation"]["SYS"]["Pao"]
        Rao = self.parameters["circulation"]["SYS"]["Rao"]
        self.var["Q_AV"] = (
            0.0
            if self.var["p_LV"] < Pao
            else (self.var["p_LV"] - self.state["p_AR_SYS"]) / Rao
        )

        EDP = self.parameters["circulation"]["SYS"]["EDP"]
        Rp = self.parameters["circulation"]["SYS"]["Rp"]
        self.var["Q_MV"] = (
            0.0
            if self.var["p_LV"] > EDP
            else (self.state["p_VEN_SYS"] - self.var["p_LV"]) / Rp
        )

    def step(self, t, dt):
        self.update_static_variables(t)

        p_ao = self.state["Pao"]
        dp_ao_dt = self.state["dp_ao_dt"]
        Q_AR_SYS = self.state["Q_AR_SYS"]
        Q_AV = self.var["Q_AV"]
        Q_MV = self.var["Q_MV"]

        p_LV = self.var["p_LV"]

        C_sys = self.parameters["circulation"]["SYS"]["Cao"]
        # Pp = self.parameters["circulation"]["SYS"]["Pp"]
        # Pao = self.parameters["circulation"]["SYS"]["Pao"]
        R_ao = self.parameters["circulation"]["SYS"]["Rao"]
        R_sys = self.parameters["circulation"]["SYS"]["Rp"]
        EDP = self.parameters["circulation"]["SYS"]["EDP"]

        Q = (p_LV - p_ao) / R_ao
        Q_R = (p_ao - EDP) / R_sys
        Q_C = C_sys * dp_ao_dt

        # Conservation of flow
        dQ_C_dt = (Q - Q_R - Q_C) / C_sys
        d2p_ao_dt2 = dQ_C_dt

        self.state["Pao"] += dt * dp_ao_dt
        self.state["dp_ao_dt"] += dt * d2p_ao_dt2
        self.state["V_LV"] += dt * (Q_MV - Q_AV)

        # self.state["p_AR_SYS"] += dt * (Pao - p_LV)
        # self.state["p_VEN_SYS"] += dt * ((Q_AR_SYS - Q_VEN_SYS) / Cao)

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
