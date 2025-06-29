import matplotlib.pyplot as plt
import numpy as np

def plot_property_vs_T(fluid, prop, Tmin, Tmax, P):
    Ts = np.linspace(Tmin, Tmax, 100)
    values = [fluid.get(prop, T, P) for T in Ts]

    fig, ax = plt.subplots()
    ax.plot(Ts, values)
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel(prop)
    ax.set_title(f"{prop} vs T for {fluid.name}")
    ax.grid(True)
    return fig