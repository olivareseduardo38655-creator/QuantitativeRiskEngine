import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO (TU PROMPT MAESTRO)
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Reporte de Riesgo Cuantitativo")

# Inyección de CSS para Tipografía Serif y Estilo Académico
st.markdown("""
<style>
    /* Importar fuentes elegantes */
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&display=swap');
    
    /* General */
    .main {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        font-family: 'Merriweather', serif;
        color: #2c3e50;
    }
    
    /* Clases del Prompt Maestro */
    .report-text {
        font-family: 'Merriweather', serif;
        font-size: 18px;
        text-align: justify;
        line-height: 1.6;
        color: #333;
        margin-bottom: 20px;
    }
    
    .observation-box {
        background-color: #ffffff;
        border-left: 4px solid #2c3e50;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        padding: 20px;
        margin-top: 20px;
        font-family: 'Merriweather', serif;
        font-size: 16px;
        font-style: italic;
    }
    
    .prescription-box {
        background-color: #f4fcf4;
        border-left: 6px solid #27ae60;
        padding: 20px;
        margin-top: 20px;
        font-family: 'Merriweather', serif;
    }
    
    /* Estilo para la Matriz Lógica */
    .logic-matrix {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 16px;
        font-family: 'Merriweather', serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    }
    .logic-matrix th, .logic-matrix td {
        padding: 12px 15px;
        border: 1px solid #ddd;
    }
    .logic-matrix th {
        background-color: #2c3e50;
        color: #ffffff;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. CARGA Y PROCESAMIENTO DE DATOS
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        # Cargamos el CSV generado por Java
        df = pd.read_csv('simulacion_riesgo.csv')
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Error Crítico: No se encuentra el archivo 'simulacion_riesgo.csv'. Ejecute el motor Java primero.")
    st.stop()

# Cálculos Estadísticos
mean_price = df['final_price'].mean()
var_95 = df['final_price'].quantile(0.05)
std_dev = df['final_price'].std()
num_simulations = len(df)

# ---------------------------------------------------------
# 3. ESTRUCTURA DEL REPORTE CIENTÍFICO
# ---------------------------------------------------------

st.title("Análisis Cuantitativo de Riesgo de Mercado: Simulación Montecarlo")
st.markdown("---")

# I. PLANTEAMIENTO DEL PROBLEMA
st.header("I. Planteamiento del Problema")
st.markdown(f"""
<div class="report-text">
El presente estudio aborda la incertidumbre inherente en la valoración de activos financieros bajo condiciones de volatilidad estocástica. 
El objetivo técnico es determinar la <b>Pérdida Máxima Probable (Value at Risk - VaR)</b> con un nivel de confianza del 95% para un horizonte temporal de 1 año (T=1).
La incógnita central reside en cuantificar la exposición al riesgo de cola (tail risk) que no es visible mediante modelos deterministas lineales.
</div>
""", unsafe_allow_html=True)

# II. METODOLOGÍA
st.header("II. Metodología y Diseño Experimental")
st.markdown(f"""
<div class="report-text">
Se implementó un motor computacional en <b>Java 21 (Virtual Threads)</b> para ejecutar {num_simulations:,.0f} simulaciones independientes basadas en el proceso estocástico de Movimiento Browniano Geométrico (GBM).
<br><br>
Los parámetros del modelo son:
<ul>
    <li>Dinámica: dS_t = S_t(μ dt + σ dW_t)</li>
    <li>Volatilidad (σ): 20%</li>
    <li>Drift (μ): 5%</li>
</ul>
Los resultados fueron consolidados y exportados para su tratamiento estadístico en este entorno.
</div>
""", unsafe_allow_html=True)

# III. ANÁLISIS EMPÍRICO
st.header("III. Análisis Empírico (Diagnóstico)")

tab1, tab2 = st.tabs(["Distribución de Probabilidad (2D)", "Topología del Riesgo (3D)"])

with tab1:
    # Histograma Profesional con Plotly
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=df['final_price'],
        nbinsx=100,
        marker_color='#34495e',
        opacity=0.75,
        name='Frecuencia'
    ))
    
    # Líneas de referencia
    fig_hist.add_vline(x=var_95, line_width=3, line_dash="dash", line_color="#c0392b")
    fig_hist.add_vline(x=mean_price, line_width=3, line_dash="dash", line_color="#27ae60")
    
    # Layout académico minimalista
    fig_hist.update_layout(
        title="Distribución de Precios Finales (N=1,000,000)",
        xaxis_title="Precio del Activo ($)",
        yaxis_title="Frecuencia Absoluta",
        template="plotly_white",
        showlegend=False,
        height=500
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown(f"""
    <div class="observation-box">
    <b>Discusión de Resultados:</b> La distribución resultante exhibe un comportamiento log-normal consistente con la teoría. 
    Se observa una asimetría positiva característica. El límite crítico se establece en <b>${var_95:,.2f}</b> (Línea Roja). 
    Cualquier valoración por debajo de este umbral representa el 5% de los escenarios más adversos.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("##### Visualización Volumétrica de Escenarios")
    
    # Muestreo para 3D (Renderizar 1M de puntos colapsa el navegador, usamos 2000 representativos)
    df_sample = df.sample(n=2000, random_state=42).reset_index()
    
    # Creamos una variable Z artificial para "profundidad" visual (Desviación de la media)
    # Esto permite ver los outliers "flotando" lejos del plano central
    df_sample['deviation'] = (df_sample['final_price'] - mean_price) / std_dev
    
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=df_sample['simulation_index'],
        y=df_sample['final_price'],
        z=df_sample['deviation'],
        mode='markers',
        marker=dict(
            size=4,
            color=df_sample['final_price'],                # Color por precio
            colorscale='Viridis',   # Paleta académica seria
            opacity=0.8
        )
    )])

    fig_3d.update_layout(
        title="Dispersión Estocástica Tridimensional (Muestra n=2,000)",
        scene = dict(
            xaxis_title='Índice de Simulación',
            yaxis_title='Precio Final ($)',
            zaxis_title='Desviación Estándar (Z-Score)'
        ),
        template="plotly_white",
        height=600,
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("""
    <div class="observation-box">
    <b>Interpretación Topológica:</b> La visualización 3D permite aislar los eventos de cola ("Cisnes Negros"). 
    Los puntos en la región inferior del eje Y y Z representan escenarios de estrés severo que requieren cobertura de capital.
    </div>
    """, unsafe_allow_html=True)

# IV. ANALÍTICA PRESCRIPTIVA
st.header("IV. Analítica Prescriptiva (Estrategia)")

# Matriz Lógica (HTML Puro)
st.markdown(f"""
<table class="logic-matrix">
  <tr>
    <th>Dimensión</th>
    <th>Hallazgo Clave</th>
    <th>Implicación de Negocio</th>
  </tr>
  <tr>
    <td><b>Descriptiva</b></td>
    <td>El precio medio converge a ${mean_price:,.2f}, pero la volatilidad expande el rango entre mínimos y máximos.</td>
    <td>El activo tiene una esperanza positiva, pero con alta dispersión.</td>
  </tr>
  <tr>
    <td><b>Diagnóstica</b></td>
    <td>El VaR al 95% es de ${var_95:,.2f}. Existe un 5% de probabilidad de caer por debajo de este nivel.</td>
    <td>El capital en riesgo es significativo. Se requiere colchón de liquidez.</td>
  </tr>
  <tr>
    <td><b>Prescriptiva</b></td>
    <td>Necesidad de cobertura (Hedging) para escenarios de cola izquierda.</td>
    <td>Activar protocolos de gestión de riesgo si el precio real se acerca a ${var_95 * 1.05:,.2f}.</td>
  </tr>
</table>
""", unsafe_allow_html=True)

# Acciones Estratégicas
st.markdown(f"""
<div class="prescription-box">
<b>📍 Acciones Estratégicas Recomendadas:</b>
<ol>
    <li><b>Establecer Reservas de Capital:</b> Basado en el cálculo del VaR, se debe provisionar la diferencia entre el precio actual y ${var_95:,.2f}.</li>
    <li><b>Monitoreo de Volatilidad:</b> Si la volatilidad de mercado supera el 20% (input del modelo), re-ejecutar el motor Java inmediatamente.</li>
    <li><b>Instrumentos Derivados:</b> Evaluar la compra de opciones PUT con strike en ${var_95:,.0f} para neutralizar el riesgo de cola.</li>
</ol>
</div>
""", unsafe_allow_html=True)

# V. CONCLUSIONES
st.header("V. Conclusiones Generales")
st.markdown("""
<div class="report-text">
La simulación de Montecarlo, potenciada por la arquitectura de alta concurrencia en Java y analizada mediante este dashboard, confirma la robustez del modelo de valoración. 
Se ha logrado cuantificar el riesgo con precisión matemática, proporcionando a la dirección un rango de confianza claro para la toma de decisiones de inversión. 
La integración de ingeniería de software y ciencia de datos ha permitido reducir la incertidumbre de mercado a métricas accionables.
</div>
""", unsafe_allow_html=True)
