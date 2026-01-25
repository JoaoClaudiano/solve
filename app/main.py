import streamlit as st
from engine.engine_api import run_beam_analysis
import json

st.set_page_config(page_title="Structural Solver", layout="wide")
st.title("Structural Solver – Viga biapoiada (exemplo)")

st.markdown(
    "Este é um exemplo mínimo mostrando a análise de uma viga biapoiada. "
    "Modifique o exemplo salvo em `examples/beam_simply_supported.json` ou carregue o seu próprio JSON."
)

# load example file
with open("examples/beam_simply_supported.json", "r", encoding="utf-8") as f:
    example = json.load(f)

st.sidebar.header("Exemplo carregado")
st.sidebar.json(example)

result = run_beam_analysis(example)

st.header("Reações")
st.write(f"Reação apoio A (x=0): {result['reactions']['A']:.3f} kN")
st.write(f"Reação apoio B (x=L): {result['reactions']['B']:.3f} kN")

st.header("Diagramas (visualização simples)")
# show small plots using matplotlib from data returned (plots created inside run_beam_analysis could be exported)
import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots()
ax1.plot(result['xs_shear'], result['shear'])
ax1.set_title("Diagrama de Esforço Cortante V(x)")
ax1.set_xlabel("x [m]")
ax1.set_ylabel("V [kN]")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(result['xs_moment'], result['moment'])
ax2.set_title("Diagrama de Momento Fletor M(x)")
ax2.set_xlabel("x [m]")
ax2.set_ylabel("M [kN·m]")
st.pyplot(fig2)

st.header("Memória de cálculo (resumo)")
st.markdown("```\n" + result['report'] + "\n```")
