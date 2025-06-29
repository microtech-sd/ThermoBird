class Pump:
    def __init__(self, inlet_P, outlet_P, inlet_T, fluid_name, efficiency=0.85):
        self.P1 = inlet_P
        self.P2 = outlet_P
        self.T1 = inlet_T
        self.fluid = fluid_name
        self.eta = efficiency

    def calculate(self):
        import CoolProp.CoolProp as CP
        h1 = CP.PropsSI("H", "T", self.T1, "P", self.P1, self.fluid)
        s1 = CP.PropsSI("S", "T", self.T1, "P", self.P1, self.fluid)
        h2s = CP.PropsSI("H", "P", self.P2, "S", s1, self.fluid)
        h2 = h1 + (h2s - h1) / self.eta
        work = h2 - h1
        return {
            "Inlet Enthalpy (h1)": h1,
            "Isentropic Outlet Enthalpy (h2s)": h2s,
            "Actual Outlet Enthalpy (h2)": h2,
            "Pump Work [J/kg]": work,
        }
