#!/usr/bin/env python3
"""
🦞 BOLT OS v2.0 - SmarterOS Control Panel 24x7
Panel operativo completo: logs + metrics pro + trends + bot control + revenue
Deploy: https://share.streamlit.io/new/deploy-from-template/b8e65aff-d8c7-4b7d-9d4c-eb79249dfc4b
Codespace: https://bookish-engine-pjwg9p75wjq5hrg7q.github.dev/
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import json
import time
from datetime import datetime, timezone, timedelta

# ============================================
# CONFIGURACIÓN
# ============================================
API_URL = os.getenv("API_URL", "http://89.116.23.167:8002")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://89.116.23.167:8003")
DB_HOST = os.getenv("DB_HOST", "89.116.23.167")
DB_NAME = os.getenv("DB_NAME", "smarter_os")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "REDACTED")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "REDACTED")

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="🦞 BOLT OS - SmarterOS",
    page_icon="🦞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SIDEBAR
# ============================================
st.sidebar.title("🦞 BOLT OS v2.0")
st.sidebar.markdown("**SmarterOS v4.1 - Control 24x7**")
st.sidebar.markdown("---")

# Auto-refresh
refresh = st.sidebar.slider("Auto-refresh (seg)", 5, 60, 10)
st.sidebar.markdown(f"⏱️ Refresh: `{refresh}s`")

# Status
st.sidebar.markdown("---")
st.sidebar.markdown("**Estado del Sistema**")

try:
    health = requests.get(f"{API_URL}/health", timeout=5).json()
    st.sidebar.success(f"✅ API Online")
    st.sidebar.caption(f"v{health.get('version', 'N/A')}")
except:
    st.sidebar.error("❌ API Offline")

# Last update
st.sidebar.markdown("---")
st.sidebar.caption(f"Última actualización: `{datetime.now().strftime('%H:%M:%S')}`")

# ============================================
# MAIN TITLE
# ============================================
st.title("🦞 BOLT OS - SmarterOS Control Panel")
st.markdown("**Sistema operativo de decisiones en producción 24x7**")

# Auto-refresh meta
st.markdown(f'<meta http-equiv="refresh" content="{refresh}">', unsafe_allow_html=True)

# ============================================
# TABS
# ============================================
tab_status, tab_events, tab_logs, tab_metrics, tab_trends, tab_bot, tab_revenue = st.tabs([
    "📊 Status",
    "🧪 Eventos",
    "🔴 Logs",
    "📈 Metrics Pro",
    "📉 Trends A7B",
    "🤖 Bot Control",
    "💰 Revenue"
])

# ============================================
# TAB 1: STATUS
# ============================================
with tab_status:
    st.header("💓 Estado del Sistema en Vivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        metrics = requests.get(f"{API_URL}/metrics", timeout=5).json()
        col1.metric("Total Eventos", metrics.get("total", 0))
        col2.metric("Avg Score", f"{metrics.get('avg_score', 0):.2f}")
        col3.metric("Valid Rate", f"{metrics.get('valid_rate', 0)*100:.1f}%")
        col4.metric("Reject Rate", f"{metrics.get('reject_rate', 0)*100:.1f}%")
    except:
        col1.metric("Total Eventos", "N/A")
        col2.metric("Avg Score", "N/A")
        col3.metric("Valid Rate", "N/A")
        col4.metric("Reject Rate", "N/A")
    
    st.markdown("---")
    st.subheader("🔌 Servicios")
    
    services = [
        ("API Smarter Food", f"{API_URL}/health"),
        ("Webhook", f"{WEBHOOK_URL}/health"),
        ("Telegram Bot", None),
    ]
    
    cols = st.columns(3)
    for i, (name, url) in enumerate(services):
        with cols[i]:
            if url:
                try:
                    r = requests.get(url, timeout=5)
                    if r.status_code < 400:
                        st.success(f"✅ {name}")
                    else:
                        st.error(f"❌ {name}")
                except:
                    st.error(f"❌ {name}")
            else:
                st.info(f"ℹ️ {name}")

# ============================================
# TAB 2: EVENTOS
# ============================================
with tab_events:
    st.header("🧪 Inyectar Eventos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Evento Manual")
        
        producto = st.selectbox("Producto", ["aluminio", "cobre", "hierro", "plastico", "papel", "vidrio"])
        precio = st.number_input("Precio (CLP)", 1000, 100000, 5000, 100)
        cantidad = st.number_input("Cantidad (kg)", 10, 2000, 100, 10)
        
        if st.button("🚀 Enviar Evento", type="primary"):
            payload = {
                "id_objeto": f"QR-{int(time.time()) % 10000}",
                "producto": producto,
                "peso_gramos": cantidad * 1000,
                "precio": precio,
                "ubicacion": "Santiago, CL"
            }
            
            try:
                r = requests.post(f"{API_URL}/api/validar", json=payload, timeout=10)
                result = r.json()
                status = result.get("status", "UNKNOWN")
                score = result.get("score", 0)
                
                if status == "VALID": st.success(f"✅ VALIDADO | Score: {score}/10")
                elif status == "SANDBOX": st.warning(f"⚠️ SOSPECHOSO | Score: {score}/10")
                elif status == "REJECTED": st.error(f"❌ INCOHERENTE | Score: {score}/10")
                else: st.info(f"📊 {status} | Score: {score}/10")
                
                st.json(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.subheader("Stress Test")
        num_events = st.slider("Número de eventos", 10, 100, 50)
        
        if st.button("🧪 Ejecutar Stress Test"):
            progress = st.progress(0)
            results = {"VALID": 0, "SANDBOX": 0, "REJECTED": 0, "ERROR": 0}
            
            for i in range(num_events):
                import random
                r = random.random()
                if r < 0.5: precio = random.uniform(3000, 7000)
                elif r < 0.8: precio = random.uniform(8000, 15000)
                else: precio = random.uniform(20000, 50000)
                
                payload = {
                    "id_objeto": f"QR-{i}",
                    "producto": random.choice(["aluminio", "cobre", "hierro"]),
                    "peso_gramos": random.uniform(50, 500),
                    "precio": round(precio, 2),
                    "ubicacion": "Santiago, CL"
                }
                
                try:
                    r = requests.post(f"{API_URL}/api/validar", json=payload, timeout=5)
                    result = r.json()
                    status = result.get("status", "ERROR")
                    results[status] = results.get(status, 0) + 1
                except:
                    results["ERROR"] += 1
                
                progress.progress((i + 1) / num_events)
            
            st.success("✅ Stress Test completado")
            
            fig = go.Figure(data=[
                go.Bar(name="VALID", x=["Count"], y=[results.get("VALID", 0)]),
                go.Bar(name="SANDBOX", x=["Count"], y=[results.get("SANDBOX", 0)]),
                go.Bar(name="REJECTED", x=["Count"], y=[results.get("REJECTED", 0)]),
            ])
            fig.update_layout(barmode="group", title="Resultados Stress Test")
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 3: LIVE LOGS
# ============================================
with tab_logs:
    st.header("🔴 Live Logs")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        log_filter = st.selectbox("Filtro", ["Todos", "VALID", "SANDBOX", "REJECTED", "ERROR"])
    with col2:
        if st.button("🔄 Refresh"): st.rerun()
    
    try:
        with open("/var/log/smarter/events.log", "r") as f:
            lines = f.readlines()[-100:]
        
        logs = []
        for line in lines:
            try:
                log = json.loads(line.strip())
                if log_filter == "Todos" or log.get("status") == log_filter:
                    logs.append(log)
            except:
                pass
        
        st.markdown(f"**{len(logs)} eventos**")
        
        for log in reversed(logs[-20:]):
            status = log.get("status", "UNKNOWN")
            score = log.get("score", 0)
            precio = log.get("precio", 0)
            producto = log.get("producto", "N/A")
            ts = log.get("ts", 0)
            
            if status == "VALID": icon = "✅"
            elif status == "SANDBOX": icon = "⚠️"
            elif status == "REJECTED": icon = "❌"
            else: icon = "❓"
            
            st.markdown(f"`{datetime.fromtimestamp(ts).strftime('%H:%M:%S')}` | {icon} **{producto}** | ${precio:,.0f} | score: {score:.1f}")
    except FileNotFoundError:
        st.info("📝 No hay logs disponibles aún")
    except Exception as e:
        st.error(f"❌ Error leyendo logs: {e}")

# ============================================
# TAB 4: METRICS PRO
# ============================================
with tab_metrics:
    st.header("📈 Metrics Pro")
    
    try:
        with open("/var/log/smarter/events.log", "r") as f:
            lines = f.readlines()
        
        events = []
        for line in lines:
            try: events.append(json.loads(line.strip()))
            except: pass
        
        if events:
            df = pd.DataFrame(events)
            
            total = len(df)
            valid_count = len(df[df["status"] == "VALID"])
            sandbox_count = len(df[df["status"] == "SANDBOX"])
            rejected_count = len(df[df["status"] == "REJECTED"])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Eventos", total)
            col2.metric("Valid Rate", f"{valid_count/total*100:.1f}%")
            col3.metric("Sandbox Rate", f"{sandbox_count/total*100:.1f}%")
            col4.metric("Reject Rate", f"{rejected_count/total*100:.1f}%")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(df, names="status", title="Distribución por Status",
                           color="status", color_discrete_map={"VALID": "#00C853", "SANDBOX": "#FFD600", "REJECTED": "#FF1744"})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(df, x="score", nbins=20, title="Distribución de Scores")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("💰 Precio vs Score")
            
            fig = px.scatter(df, x="precio", y="score", color="status",
                           title="Relación Precio vs Score",
                           color_discrete_map={"VALID": "#00C853", "SANDBOX": "#FFD600", "REJECTED": "#FF1744"})
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🧠 Policy Engine Indicators")
            
            sandbox_rate = sandbox_count / total if total > 0 else 0
            reject_rate = rejected_count / total if total > 0 else 0
            avg_score = df["score"].mean() if "score" in df.columns else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sandbox Rate", f"{sandbox_rate*100:.1f}%")
                st.progress(min(sandbox_rate / 0.35, 1.0))
            with col2:
                st.metric("Reject Rate", f"{reject_rate*100:.1f}%")
                st.progress(min(reject_rate / 0.25, 1.0))
            with col3:
                st.metric("Avg Score", f"{avg_score:.2f}")
                st.progress(min(avg_score / 10.0, 1.0))
            
            st.markdown("---")
            st.subheader("⚙️ Policy Actions")
            
            actions = []
            if sandbox_rate > 0.35: actions.append("⚠️ adjust_warn → sandbox_rate > 35%")
            if reject_rate > 0.25: actions.append("🔴 tighten_validation → reject_rate > 25%")
            if avg_score < 6.5: actions.append("📉 alert_low_score → avg_score < 6.5")
            if avg_score > 8.0 and sandbox_rate < 0.2: actions.append("📈 relax_validation → high scores, low sandbox")
            
            if actions:
                for action in actions: st.warning(action)
            else:
                st.success("✅ No policy actions needed")
        else:
            st.info("📝 No hay eventos aún")
    except FileNotFoundError:
        st.info("📝 No hay logs disponibles")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ============================================
# TAB 5: TRENDS A7B
# ============================================
with tab_trends:
    st.header("📉 Análisis de Comportamiento del Loop A7B")
    
    try:
        with open("/var/log/smarter/events.log", "r") as f:
            lines = f.readlines()
        
        events = []
        for line in lines:
            try: events.append(json.loads(line.strip()))
            except: pass
        
        if events:
            df = pd.DataFrame(events)
            df["timestamp"] = pd.to_datetime(df["ts"], unit="s")
            df["hour"] = df["timestamp"].dt.hour
            
            # Hourly aggregation
            hourly = df.groupby("hour").agg(
                total_events=("ts", "count"),
                avg_score=("score", "mean"),
                valid_count=("status", lambda x: (x == "VALID").sum()),
                sandbox_count=("status", lambda x: (x == "SANDBOX").sum()),
                rejected_count=("status", lambda x: (x == "REJECTED").sum())
            ).reset_index()
            
            hourly["valid_rate"] = hourly["valid_count"] / hourly["total_events"]
            hourly["sandbox_rate"] = hourly["sandbox_count"] / hourly["total_events"]
            hourly["reject_rate"] = hourly["rejected_count"] / hourly["total_events"]
            
            # Score evolution
            st.subheader("📊 Evolución de Validación A7B")
            
            fig = px.line(hourly, x="hour", y="avg_score",
                         title="Evolución de Score Promedio por Hora",
                         template="plotly_dark", markers=True)
            fig.add_hline(y=6.5, line_dash="dash", line_color="red", annotation_text="Threshold")
            st.plotly_chart(fig, use_container_width=True)
            
            # Rates evolution
            st.subheader("📈 Tasas por Hora")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hourly["hour"], y=hourly["valid_rate"], name="Valid Rate", line=dict(color="green")))
            fig.add_trace(go.Scatter(x=hourly["hour"], y=hourly["sandbox_rate"], name="Sandbox Rate", line=dict(color="yellow")))
            fig.add_trace(go.Scatter(x=hourly["hour"], y=hourly["reject_rate"], name="Reject Rate", line=dict(color="red")))
            fig.update_layout(title="Tasas de Validación por Hora", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume
            st.subheader("📊 Volumen de Eventos por Hora")
            
            fig = px.bar(hourly, x="hour", y="total_events", title="Eventos por Hora", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Product breakdown
            st.subheader("📦 Distribución por Producto")
            
            if "producto" in df.columns:
                product_stats = df.groupby("producto").agg(
                    count=("ts", "count"),
                    avg_score=("score", "mean"),
                    avg_precio=("precio", "mean")
                ).reset_index()
                
                fig = px.scatter(product_stats, x="avg_precio", y="avg_score", size="count",
                               color="producto", title="Score vs Precio por Producto",
                               template="plotly_dark", hover_data=["count"])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📝 No hay datos para trends")
    except FileNotFoundError:
        st.info("📝 No hay logs disponibles")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ============================================
# TAB 6: BOT CONTROL
# ============================================
with tab_bot:
    st.header("🤖 Bot Control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Enviar Mensaje")
        message = st.text_area("Mensaje", "🦞 SmarterOS Status: All systems operational")
        chat_id = st.text_input("Chat ID", TELEGRAM_CHAT_ID)
        
        if st.button("📤 Enviar a Telegram", type="primary"):
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                r = requests.post(url, json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }, timeout=5)
                
                if r.json().get("ok"): st.success("✅ Mensaje enviado")
                else: st.error(f"❌ Error: {r.json()}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.subheader("🔔 Alertas Automáticas")
        st.toggle("Alertas de sistema", value=True)
        st.toggle("Alertas de policy engine", value=True)
        st.toggle("Alertas de revenue", value=False)
        
        st.markdown("---")
        st.markdown("**Últimas alertas enviadas:**")
        st.caption("No hay alertas recientes")

# ============================================
# TAB 7: REVENUE
# ============================================
with tab_revenue:
    st.header("💰 Revenue Estimator")
    
    try:
        with open("/var/log/smarter/events.log", "r") as f:
            lines = f.readlines()
        
        events = []
        for line in lines:
            try: events.append(json.loads(line.strip()))
            except: pass
        
        if events:
            df = pd.DataFrame(events)
            
            total_events = len(df)
            avg_price = df["precio"].mean() if "precio" in df.columns else 0
            valid_events = len(df[df["status"] == "VALID"])
            
            base_revenue = valid_events * 10
            transaction_revenue = df[df["status"] == "VALID"]["precio"].sum() * 0.001 if "precio" in df.columns else 0
            total_revenue = base_revenue + transaction_revenue
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Eventos", total_events)
            col2.metric("Eventos Válidos", valid_events)
            col3.metric("Avg Precio", f"${avg_price:,.0f}")
            col4.metric("Revenue Est.", f"${total_revenue:,.0f} CLP")
            
            st.markdown("---")
            st.subheader("📊 Revenue Breakdown")
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Base Revenue", x=["Revenue"], y=[base_revenue]))
            fig.add_trace(go.Bar(name="Transaction %", x=["Revenue"], y=[transaction_revenue]))
            fig.update_layout(barmode="stack", title="Revenue Composition")
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.subheader("📈 Proyección Mensual")
            
            monthly_revenue = total_revenue * 30
            st.metric("Revenue Mensual Estimado", f"${monthly_revenue:,.0f} CLP")
        else:
            st.info("📝 No hay datos para calcular revenue")
    except FileNotFoundError:
        st.info("📝 No hay logs disponibles")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(
    f"**🦞 BOLT OS v2.0** | SmarterOS v4.1 | "
    f"Actualizado: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}` | "
    f"API: `{API_URL}` | "
    f"Codespace: [bookish-engine](https://bookish-engine-pjwg9p75wjq5hrg7q.github.dev/)"
)

# ============================================
# COGNITIVE LAYER TAB (v4.3)
# ============================================
with st.expander("🧠 Cognitive Layer (v4.3)"):
    st.subheader("🧠 Capa Cognitiva - Estado de Activación")
    
    try:
        # Get cognitive status from API
        cognitive_status = requests.get(f"{API_URL}/cognitive/status", timeout=5).json()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Ready to Activate",
                "✅ YES" if cognitive_status.get("ready") else "⏳ NO",
                f"{cognitive_status.get('conditions_met', 0)}/{cognitive_status.get('conditions_total', 3)} conditions"
            )
        
        with col2:
            st.metric(
                "Total Events",
                cognitive_status.get("total_events", 0),
                "Target: 200"
            )
        
        with col3:
            st.metric(
                "Real Events",
                cognitive_status.get("real_events", 0),
                "Target: 50"
            )
        
        st.markdown("---")
        
        # Progress bars
        st.subheader("📊 Activation Conditions")
        
        total = cognitive_status.get("total_events", 0)
        real = cognitive_status.get("real_events", 0)
        sandbox = cognitive_status.get("sandbox_rate", 0)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Events", f"{total}/200")
            st.progress(min(total / 200, 1.0))
        
        with col2:
            st.metric("Real Events", f"{real}/50")
            st.progress(min(real / 50, 1.0))
        
        with col3:
            st.metric("Sandbox Rate", f"{sandbox}%")
            st.progress(min(sandbox / 45, 1.0) if sandbox <= 45 else 1.0)
        
        st.markdown("---")
        
        # Cognitive layer status
        st.subheader("🔌 Cognitive Services")
        
        cog_layer = cognitive_status.get("cognitive_layer", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            bookish = cog_layer.get("bookish", {})
            if bookish.get("available"):
                st.success(f"✅ Bookish ({bookish.get('mode', 'unknown')})")
            else:
                st.error("❌ Bookish (offline)")
        
        with col2:
            emdash = cog_layer.get("emdash", {})
            if emdash.get("available"):
                st.success(f"✅ Emdash ({emdash.get('mode', 'unknown')})")
            else:
                st.error("❌ Emdash (offline)")
        
        # Activation instructions
        if cognitive_status.get("ready"):
            st.success("🚀 Cognitive layer is ready to activate!")
            st.code("docker compose --profile cognitive up -d", language="bash")
        else:
            st.info("⏳ Continue capturing events to activate cognitive layer")
            st.markdown(f"**Missing:** {3 - cognitive_status.get('conditions_met', 0)} conditions")
    
    except Exception as e:
        st.error(f"❌ Error fetching cognitive status: {e}")
        st.info("💡 Cognitive layer status will appear here when API is available")
