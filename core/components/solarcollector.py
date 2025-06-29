class SolarThermalCollector:
    def __init__(self, inlet_T, outlet_T, fluid_name, efficiency=0.7, solar_irradiance=800):
        self.T1 = inlet_T
        self.T2 = outlet_T
        self.fluid = fluid_name
        self.eta = efficiency
        self.G = solar_irradiance  # W/m²

    def calculate(self):
        import CoolProp.CoolProp as CP
        cp = CP.PropsSI("C", "T", (self.T1+self.T2)/2, "P", 101325, self.fluid)
        q = self.eta * self.G  # Simplified power absorbed per unit area
        mass_flow_rate = 1  # kg/s (assumed unit flow)
        heat_gain = mass_flow_rate * cp * (self.T2 - self.T1)
        efficiency_calc = heat_gain / (self.G * 1)  # Area=1 m² assumed
        return {
            "Heat Gain [W]": heat_gain,
            "Collector Efficiency": efficiency_calc,
            "Input Power [W/m²]": self.G,
        }
