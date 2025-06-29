class ExpansionValve:
    def __init__(self, inlet_P, outlet_P, inlet_T, fluid_name):
        self.P1 = inlet_P
        self.P2 = outlet_P
        self.T1 = inlet_T
        self.fluid = fluid_name

    def calculate(self):
        import CoolProp.CoolProp as CP
        h1 = CP.PropsSI("H", "T", self.T1, "P", self.P1, self.fluid)
        # Assume isenthalpic expansion (constant enthalpy)
        h2 = h1
        T2 = CP.PropsSI("T", "P", self.P2, "H", h2, self.fluid)
        return {
            "Inlet Enthalpy (h1)": h1,
            "Outlet Enthalpy (h2)": h2,
            "Outlet Temperature (T2)": T2,
        }
