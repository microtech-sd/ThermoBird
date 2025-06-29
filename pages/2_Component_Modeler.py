import streamlit as st
from core.components.compressor import Compressor
from core.components.turbine import Turbine
# Add others as needed:
# from core.components.pump import Pump
# from core.components.evaporator import Evaporator


st.header("🔧 Component Modeler")

# Step 1: Dropdown to choose the component
component_choice = st.selectbox("Select a Component", [
    "Compressor", "Turbine", "Evaporator", "Pump", "Heater", "Condenser"
])

# Step 2: Universal inputs (extend as needed)
fluid = st.selectbox("Fluid", ["Water", "R134a", "Ammonia"], key="component_fluid")
P1 = st.number_input("Inlet Pressure [Pa]", 1e5, 5e6, 1e5)
P2 = st.number_input("Outlet Pressure [Pa]", 1e5, 5e6, 2e5)
T1 = st.number_input("Inlet Temperature [K]", 250.0, 800.0, 300.0)
eta = st.slider("Isentropic Efficiency", 0.5, 1.0, 0.85)

# Step 3: Run logic dynamically
if st.button("🧠 Run Component"):
    if component_choice == "Compressor":
        comp = Compressor(P1, P2, T1, fluid, eta)
        results = comp.calculate()

    elif component_choice == "Turbine":
        turbine = Turbine(P1, P2, T1, fluid, eta)
        results = turbine.calculate()

    # You can add additional components like this:
    # elif component_choice == "Evaporator":
    #     from core.components.evaporator import Evaporator
    #     evap = Evaporator(...)
    #     results = evap.calculate()

    # Display results
    for key, value in results.items():
        st.write(f"**{key}:** {value:.2f}")
