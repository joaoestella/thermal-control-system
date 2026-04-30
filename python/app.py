import streamlit as st
import serial
import time
import pandas as pd
from datetime import datetime

# 1. Configuração de Estilo e Layout
st.set_page_config(
    page_title="FIAP | Monitoramento Térmico",
    page_icon="🔥",
    layout="wide"
)

# CSS Ajustado para Dark Mode (Sem blocos brancos)
st.markdown("""
    <style>
    .stMetric { 
        background-color: #1E1E1E; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #333;
    }
    [data-testid="stMetricValue"] { color: #00FF00 !important; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização da Serial
if 'arduino' not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial("COM5", 9600, timeout=0.1)
        time.sleep(2)
    except:
        st.session_state.arduino = None

if 'df_temp' not in st.session_state:
    st.session_state.df_temp = pd.DataFrame(columns=['Hora', 'Temperatura'])

# --- TELA PRINCIPAL ---
st.title("🌡️ Sistema de Controle Térmico PWM")
st.caption("Projeto FIAP - Engenharia de Computação | Monitoramento em Tempo Real (1Hz)")

col_grafico, col_controle = st.columns([2, 1])

with col_controle:
    st.subheader("🎮 Painel de Controle")
    
    porcentagem = st.slider("Definir Potência (%)", 0, 100, 0)
    
    ton = (porcentagem / 100) * 30
    toff = 30 - ton
    
    # Métricas de tempo sem fundo branco
    c1, c2 = st.columns(2)
    c1.metric("Tempo ON", f"{ton:.1f}s")
    c2.metric("Tempo OFF", f"{toff:.1f}s")
    
    if st.button("APLICAR POTÊNCIA", use_container_width=True, type="primary"):
        if st.session_state.arduino:
            try:
                st.session_state.arduino.write(f"{porcentagem}\n".encode())
                st.toast(f"Potência: {porcentagem}%", icon="✅")
            except:
                st.error("Erro na Serial")

with col_grafico:
    st.subheader("📈 Gráfico de Telemetria")
    placeholder_metrica = st.empty()
    placeholder_grafico = st.empty()

# Loop de Leitura
while True:
    if st.session_state.arduino:
        try:
            if st.session_state.arduino.in_waiting > 0:
                linha = st.session_state.arduino.readline().decode("utf-8").strip()
                if linha:
                    temp_val = float(linha)
                    agora = datetime.now().strftime("%H:%M:%S")
                    
                    novo_dado = pd.DataFrame({'Hora': [agora], 'Temperatura': [temp_val]})
                    st.session_state.df_temp = pd.concat([st.session_state.df_temp, novo_dado], ignore_index=True)
                    
                    if len(st.session_state.df_temp) > 20:
                        st.session_state.df_temp = st.session_state.df_temp.iloc[1:]
                    
                    with placeholder_metrica:
                        st.metric(label="Temperatura Atual", value=f"{temp_val} °C")
                    
                    with placeholder_grafico:
                        # Usando line_chart para a leitura ficar mais clara que o area_chart
                        st.line_chart(
                            st.session_state.df_temp.set_index('Hora'),
                            height=400
                        )
        except Exception:
            pass
            
    time.sleep(1)