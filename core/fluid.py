import CoolProp.CoolProp as CP

class Fluid:
    def __init__(self, name: str):
        self.name = name

    def get(self, prop: str, T: float, P: float) -> float:
        return CP.PropsSI(prop, "T", T, "P", P, self.name)