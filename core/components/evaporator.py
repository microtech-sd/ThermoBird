class Evaporator:
    def __init__(self, inlet_T, outlet_T, inlet_P, outlet_P, fluid_name, heat_transfer_rate=None):
        self.T1 = inlet_T
        self.T2 = outlet_T
        self.P1 = inlet_P
        self.P2 = outlet_P
        self.fluid = fluid_name
        self.q = heat_transfer_rate  # Optional input

    def calculate(self):
        # Placeholder: Heat absorbed in evaporation
        import CoolProp.CoolProp as CP
        h1 = CP.PropsSI("H", "T", self.T1, "P", self.P1, self.fluid)
        h2 = CP.PropsSI("H", "T", self.T2, "P", self.P2, self.fluid)
        q_calc = h2 - h1
        return {
            "Enthalpy Inlet (h1)": h1,
            "Enthalpy Outlet (h2)": h2,
            "Heat Transfer Rate (Q) [J/kg]": q_calc if self.q is None else self.q,
        }
