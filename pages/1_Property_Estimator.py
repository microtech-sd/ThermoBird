import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from CoolProp.CoolProp import PropsSI, PhaseSI

# Page config
st.set_page_config(page_title="Fluid Property Estimator", layout="wide")
st.markdown("# 🧪 Fluid Property Estimator")
st.markdown("Estimate thermodynamic state points, visualize property diagrams, and export fluid data.")

# --- Sidebar Config ---
with st.sidebar:
    fluid = st.selectbox("🌡️ Select Fluid", ["Water", "R134a", "Ammonia", "CO2", "Air"])
    unit_system = st.radio("⚙️ Unit System", ["SI", "Imperial"], horizontal=True)

# --- Unit Conversion Functions ---
def convert_units(prop, value, system):
    if system == "SI":
        return value
    conversions = {
        "T": lambda v: v * 9/5 - 459.67,
        "P": lambda v: v / 1000 if system == "SI" else v / 6894.76,
        "H": lambda v: v / 2326,
        "S": lambda v: v / 4186.8,
        "U": lambda v: v / 2326,
        "Cp": lambda v: v / 4186.8,
        "Cv": lambda v: v / 4186.8,
        "D": lambda v: v / 16.0185,
        "V": lambda v: v * 16.0185,
        "M": lambda v: v * 1000 / 453.592,
        "VISCOSITY": lambda v: v * 0.000672,
        "CONDUCTIVITY": lambda v: v * 0.5779
    }
    return conversions.get(prop, lambda x: x)(value)

units = {
    "T": "K" if unit_system == "SI" else "°F",
    "P": "kPa" if unit_system == "SI" else "psi",
    "H": "kJ/kg" if unit_system == "SI" else "Btu/lb",
    "S": "kJ/kg.K" if unit_system == "SI" else "Btu/lb.R",
    "U": "kJ/kg" if unit_system == "SI" else "Btu/lb",
    "Cp": "kJ/kg.K" if unit_system == "SI" else "Btu/lb.R",
    "Cv": "kJ/kg.K" if unit_system == "SI" else "Btu/lb.R",
    "D": "kg/m³" if unit_system == "SI" else "lb/ft³",
    "V": "m³/kg" if unit_system == "SI" else "ft³/lb",
    "M": "kg/mol" if unit_system == "SI" else "lb/mol",
    "VISCOSITY": "Pa.s" if unit_system == "SI" else "lb/ft.hr",
    "CONDUCTIVITY": "W/m.K" if unit_system == "SI" else "Btu/hr.ft.R",
    "Z": "-",
    "Phase": "",
    "Quality": "-"
}

# --- Layout ---
col_left, col_right = st.columns(2)

# --- Left: State Property Calculator ---
with col_left:
    st.markdown("## 🔍 State Solver")
    props = ["T", "P", "H", "S", "Q"]
    known1 = st.selectbox("Property 1", props, key="k1")
    val1 = st.number_input(f"{known1} ({units[known1]})", key="v1")
    known2 = st.selectbox("Property 2", [p for p in props if p != known1], key="k2")
    val2 = st.number_input(f"{known2} ({units[known2]})", key="v2")

    if st.button("🔬 Compute State"):
        try:
            state = {
                "T": PropsSI("T", known1, val1, known2, val2, fluid),
                "P": PropsSI("P", known1, val1, known2, val2, fluid),
                "H": PropsSI("H", known1, val1, known2, val2, fluid),
                "S": PropsSI("S", known1, val1, known2, val2, fluid),
                "U": PropsSI("U", known1, val1, known2, val2, fluid),
                "D": PropsSI("D", known1, val1, known2, val2, fluid),
                "Cp": PropsSI("C", known1, val1, known2, val2, fluid),
                "Cv": PropsSI("O", known1, val1, known2, val2, fluid),
                "VISCOSITY": PropsSI("VISCOSITY", known1, val1, known2, val2, fluid),
                "CONDUCTIVITY": PropsSI("CONDUCTIVITY", known1, val1, known2, val2, fluid),
                "Z": PropsSI("Z", known1, val1, known2, val2, fluid),
                "M": PropsSI("M", fluid),
                "Phase": PhaseSI("T", PropsSI("T", known1, val1, known2, val2, fluid), "P", PropsSI("P", known1, val1, known2, val2, fluid), fluid)
            }

            rho = state["D"]
            state["V"] = 1 / rho if rho else None

            df = pd.DataFrame({
                "Property": list(state.keys()),
                "Value": [convert_units(p, state[p], unit_system) for p in state],
                "Unit": [units[p] for p in state]
            })
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode()
            xlsx = io.BytesIO()
            with pd.ExcelWriter(xlsx, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 Download CSV", csv, "state_data.csv")
            st.download_button("📥 Download Excel", xlsx.getvalue(), "state_data.xlsx")

        except Exception as e:
            st.error(f"Calculation failed: {e}")

# --- Right: Plot Section ---
with col_right:
    st.markdown("## 📊 Thermodynamic Diagrams")
    diagram = st.radio("Select Diagram", ["T-s", "P-v", "H-s"], horizontal=True)

    if st.button("📈 Generate Plot"):
        try:
            T_range = [300 + i * 20 for i in range(10)]
            results = {"T": [], "P": [], "H": [], "S": [], "V": []}
            for T in T_range:
                try:
                    P = PropsSI("P", "T", T, "Q", 1, fluid)
                    H = PropsSI("H", "T", T, "Q", 1, fluid)
                    S = PropsSI("S", "T", T, "Q", 1, fluid)
                    D = PropsSI("D", "T", T, "Q", 1, fluid)
                    V = 1 / D if D else None
                    results["T"].append(T)
                    results["P"].append(P)
                    results["H"].append(H)
                    results["S"].append(S)
                    results["V"].append(V)
                except:
                    continue

            fig, ax = plt.subplots()
            if diagram == "T-s":
                ax.plot(results["S"], results["T"], label=f"{fluid} - T-s")
                ax.set_xlabel(f"Entropy [{units['S']}]")
                ax.set_ylabel(f"Temperature [{units['T']}]")
            elif diagram == "P-v":
                ax.plot(results["V"], results["P"], label=f"{fluid} - P-v")
                ax.set_xlabel(f"Specific Volume [{units['V']}]")
                ax.set_ylabel(f"Pressure [{units['P']}]")
            elif diagram == "H-s":
                ax.plot(results["S"], results["H"], label=f"{fluid} - H-s")
                ax.set_xlabel(f"Entropy [{units['S']}]")
                ax.set_ylabel(f"Enthalpy [{units['H']}]")
            ax.legend()
            ax.grid()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Plot failed: {e}")
