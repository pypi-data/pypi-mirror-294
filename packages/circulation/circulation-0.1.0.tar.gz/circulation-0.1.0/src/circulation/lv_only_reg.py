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
        valves = self.parameters["valves"]

        if self._add_units:
            unit_R = 1 * mmHg * s / mL
            unit_p = 1 * mmHg
        else:
            unit_R = 1
            unit_p = 1

        self.R_AV = self._R(
            valves["AV"]["Rmin"], valves["AV"]["Rmax"], unit_R=unit_R, unit_p=unit_p
        )
        self.R_MV = self._R(
            valves["MV"]["Rmin"], valves["MV"]["Rmax"], unit_R=unit_R, unit_p=unit_p
        )

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
            "valves": {
                "MV": {
                    "Rmin": 0.0075 * mmHg * s / mL,
                    "Rmax": 75006.2 * mmHg * s / mL,
                },
                "AV": {
                    "Rmin": 0.0075 * mmHg * s / mL,
                    "Rmax": 75006.2 * mmHg * s / mL,
                },
            },
            "circulation": {
                "SYS": {
                    "R_AR": 0.8 * mmHg * s / mL,
                    "C_AR": 1.2 * mL / mmHg,
                    "R_VEN": 0.26 * mmHg * s / mL,
                    "C_VEN": 60.0 * mL / mmHg,
                    "L_AR": 5e-3 * mmHg * s**2 / mL,
                    "L_VEN": 5e-4 * mmHg * s**2 / mL,
                },
            },
        }

    @staticmethod
    def default_initial_conditions() -> dict[str, float]:
        return {
            "V_LA": 65.0 * mL,
            "V_LV": 120.0 * mL,
            "V_RA": 65.0 * mL,
            "V_RV": 145.0 * mL,
            "p_AR_SYS": 80.0 * mmHg,
            "p_VEN_SYS": 30.0 * mmHg,
            "p_AR_PUL": 35.0 * mmHg,
            "p_VEN_PUL": 24.0 * mmHg,
            "Q_AR_SYS": 0.0 * mL / s,
            "Q_VEN_SYS": 0.0 * mL / s,
            "Q_AR_PUL": 0.0 * mL / s,
            "Q_VEN_PUL": 0.0 * mL / s,
        }

    def update_static_variables(self, t):
        self.var["p_LV"] = self.p_LV_func(self.state["V_LV"], t)
        self.var["Q_AV"] = self.flux_through_valve(
            self.var["p_LV"], self.state["p_AR_SYS"], self.R_AV
        )
        self.var["Q_MV"] = self.flux_through_valve(
            self.state["p_VEN_SYS"], self.var["p_LV"], self.R_MV
        )

    def step(self, t, dt):
        self.update_static_variables(t)

        Q_VEN_SYS = self.state["Q_VEN_SYS"]
        Q_AR_SYS = self.state["Q_AR_SYS"]
        Q_AV = self.var["Q_AV"]
        Q_MV = self.var["Q_MV"]

        p_LV = self.var["p_LV"]
        p_AR_SYS = self.state["p_AR_SYS"]
        p_VEN_SYS = self.state["p_VEN_SYS"]

        C_VEN_SYS = self.parameters["circulation"]["SYS"]["C_VEN"]
        C_AR_SYS = self.parameters["circulation"]["SYS"]["C_AR"]
        R_AR_SYS = self.parameters["circulation"]["SYS"]["R_AR"]
        R_VEN_SYS = self.parameters["circulation"]["SYS"]["R_VEN"]
        L_AR_SYS = self.parameters["circulation"]["SYS"]["L_AR"]
        L_VEN_SYS = self.parameters["circulation"]["SYS"]["L_VEN"]

        self.state["V_LV"] += dt * (Q_MV - Q_AV)

        self.state["p_AR_SYS"] += dt * (Q_AV - Q_AR_SYS) / C_AR_SYS
        self.state["p_VEN_SYS"] += dt * (Q_AR_SYS - Q_VEN_SYS) / C_VEN_SYS
        self.state["Q_AR_SYS"] += (
            -dt * (R_AR_SYS * Q_AR_SYS + p_VEN_SYS - p_AR_SYS) / L_AR_SYS
        )
        self.state["Q_VEN_SYS"] += (
            -dt * (R_VEN_SYS * Q_VEN_SYS + p_LV - p_VEN_SYS) / L_VEN_SYS
        )

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
