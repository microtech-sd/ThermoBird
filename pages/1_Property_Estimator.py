import streamlit as st
from core.fluid import Fluid
from core.plot import plot_property_vs_T

st.header("📊 Property Estimator")
fluid_name: object = st.selectbox("Select a fluid", ["Water", "R134a", "Ammonia"], key="estimator_fluid")
prop = st.selectbox("Property", ["C", "D", "H", "S", "L", "VISCOSITY"])
T = st.number_input("Temperature [K]", 300.0, 1000.0, 350.0)
P = st.number_input("Pressure [Pa]", 1e5, 2e6, 101325.0)

fluid = Fluid(fluid_name)
value = fluid.get(prop, T, P)
st.metric(f"{prop} at {T} K, {P/1e5:.2f} bar", f"{value:.2f}")

if st.checkbox("📈 Plot vs Temperature"):
        Tmin = st.slider("Min Temp (K)", 250, 1000, 300)
        Tmax = st.slider("Max Temp (K)", Tmin+10, 1200, 600)
        fig = plot_property_vs_T(fluid, prop, Tmin, Tmax, P)
        st.pyplot(fig)