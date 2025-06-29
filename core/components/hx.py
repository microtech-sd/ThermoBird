class HeatExchanger:
    def __init__(self, hot_in_T, hot_out_T, cold_in_T, cold_out_T, fluid_hot, fluid_cold, heat_transfer_rate=None):
        self.Th_in = hot_in_T
        self.Th_out = hot_out_T
        self.Tc_in = cold_in_T
        self.Tc_out = cold_out_T
        self.fluid_hot = fluid_hot
        self.fluid_cold = fluid_cold
        self.q = heat_transfer_rate

    def calculate(self):
        import CoolProp.CoolProp as CP
        h_hot_in = CP.PropsSI("H", "T", self.Th_in, "P", 101325, self.fluid_hot)
        h_hot_out = CP.PropsSI("H", "T", self.Th_out, "P", 101325, self.fluid_hot)
        h_cold_in = CP.PropsSI("H", "T", self.Tc_in, "P", 101325, self.fluid_cold)
        h_cold_out = CP.PropsSI("H", "T", self.Tc_out, "P", 101325, self.fluid_cold)

        q_hot = h_hot_in - h_hot_out
        q_cold = h_cold_out - h_cold_in
        return {
            "Heat Lost by Hot Fluid [J/kg]": q_hot,
            "Heat Gained by Cold Fluid [J/kg]": q_cold,
            "Heat Transfer [J/kg]": self.q if self.q is not None else min(q_hot, q_cold),
        }
