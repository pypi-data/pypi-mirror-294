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
        self.p_LV_func = lambda V, t: self.E_LV(t) * (V - chambers["LV"]["V0"])
        self.var = {}

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

    def update_static_variables(self, t):
        self.var["p_LV"] = self.p_LV_func(self.state["V_LV"], t)

    def step(self, t, dt):
        self.update_static_variables(t)

        p_ao = self.state["p_ao"]
        dp_ao_dt = self.state["dp_ao_dt"]
        p_LV = self.var["p_LV"]

        C_sys = self.parameters["circulation"]["SYS"]["C_sys"]
        R_ao = self.parameters["circulation"]["SYS"]["Rao"]
        R_sys = self.parameters["circulation"]["SYS"]["R_sys"]
        p_dia = self.parameters["circulation"]["SYS"]["p_dia"]

        Q = (p_LV - p_ao) / R_ao
        Q_R = (p_ao - p_dia) / R_sys
        Q_C = C_sys * dp_ao_dt

        dQ_C_dt = (Q - Q_R - Q_C) / C_sys
        d2p_ao_dt2 = dQ_C_dt

        self.state["p_ao"] += dt * dp_ao_dt
        self.state["dp_ao_dt"] += dt * d2p_ao_dt2
        if p_LV > p_ao:
            self.state["V_LV"] += -dt * Q

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
