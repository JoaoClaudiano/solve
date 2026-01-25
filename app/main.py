import streamlit as st
import json
import matplotlib.pyplot as plt

from engine.engine_api import run_beam_analysis

st.set_page_config(
    page_title="Structural Solver – Vigas",
    layout="wide"
)

st.title("Structural Solver – Análise de Vigas (Didático)")

st.markdown(
    """
    Esta aplicação tem caráter **didático**, voltada para alunos de Engenharia Civil.
    Os cálculos apresentados seguem rigorosamente as equações de equilíbrio da estática
    e são mostrados passo a passo para facilitar o aprendizado.
    """
)

# -------------------------------------------------
# Entrada de dados
# -------------------------------------------------
st.header("1. Dados de entrada")

with open("examples/beam_simply_supported.json", "r", encoding="utf-8") as f:
    example = json.load(f)

st.markdown("Exemplo carregado automaticamente:")
st.json(example)

# -------------------------------------------------
# Processamento
# -------------------------------------------------
result = run_beam_analysis(example)

# -------------------------------------------------
# Modelo estrutural
# -------------------------------------------------
st.header("2. Modelo estrutural adotado")

st.markdown(
    f"""
    ```
    [A]────────────────────────────[B]
     ↑ RA                           ↑ RB
     ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
           cargas aplicadas
    ```

    - Tipo: viga biapoiada
    - Comprimento: **L = {result['length']:.2f} m**
    - Apoio A em x = 0 m
    - Apoio B em x = L
    """
)

# -------------------------------------------------
# Memória de cálculo (blocos)
# -------------------------------------------------
st.header("3. Memória de cálculo")

report_lines = result["report"].split("\n")

sections = {
    "1. DADOS DO PROBLEMA": [],
    "2. MODELO ESTRUTURAL ADOTADO": [],
    "3. CÁLCULO DAS REAÇÕES DE APOIO": [],
    "4. APLICAÇÃO DAS EQUAÇÕES DE EQUILÍBRIO": [],
    "5. RESULTADOS FINAIS": []
}

current_section = None

for line in report_lines:
    line = line.strip()
    if line in sections:
        current_section = line
    elif current_section:
        sections[current_section].append(line)

for title, content in sections.items():
    with st.expander(title, expanded=(title == "1. DADOS DO PROBLEMA")):
        st.text("\n".join(content))

# -------------------------------------------------
# Resultados numéricos
# -------------------------------------------------
st.header("4. Resultados")

col1, col2 = st.columns(2)

with col1:
    st.metric("Reação no apoio A (RA)", f"{result['reactions']['A']:.2f} kN")

with col2:
    st.metric("Reação no apoio B (RB)", f"{result['reactions']['B']:.2f} kN")

# -------------------------------------------------
# Diagramas
# -------------------------------------------------
st.header("5. Diagramas")

fig_v, ax_v = plt.subplots()
ax_v.plot(result["xs_shear"], result["shear"])
ax_v.set_title("Diagrama de Esforço Cortante V(x)")
ax_v.set_xlabel("x [m]")
ax_v.set_ylabel("V [kN]")
st.pyplot(fig_v)

fig_m, ax_m = plt.subplots()
ax_m.plot(result["xs_moment"], result["moment"])
ax_m.set_title("Diagrama de Momento Fletor M(x)")
ax_m.set_xlabel("x [m]")
ax_m.set_ylabel("M [kN·m]")
st.pyplot(fig_m)

st.markdown(
    """
    **Observação:** os diagramas apresentados são coerentes com os resultados das
    reações de apoio e com o comportamento físico esperado da viga.
    """
)
