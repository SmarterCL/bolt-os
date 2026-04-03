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
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

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

# ============================================
# 🍔 FOOD ORDERING TAB — Just Burger Style
# ============================================
with st.expander("🍔 Pedir Comida — Just Burger Style"):
    st.markdown("""
    <style>
    /* Just Burger Style Overrides */
    .jb-promo-banner {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        padding: 15px 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        color: #0f172a;
    }
    .jb-promo-banner h3 {
        margin: 0 0 5px 0;
        font-size: 1.3rem;
        font-weight: 900;
    }
    .jb-promo-banner p {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .jb-category-tabs {
        display: flex;
        gap: 10px;
        overflow-x: auto;
        padding: 10px 0;
        margin-bottom: 20px;
        border-bottom: 2px solid #334155;
    }
    .jb-category-tab {
        padding: 10px 20px;
        background: #1e293b;
        border: 2px solid #334155;
        border-radius: 25px;
        cursor: pointer;
        white-space: nowrap;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .jb-category-tab:hover, .jb-category-tab.active {
        background: #fbbf24;
        border-color: #fbbf24;
        color: #0f172a;
    }
    .jb-product-card {
        background: #1e293b;
        border: 2px solid #334155;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .jb-product-card:hover {
        border-color: #fbbf24;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(251, 191, 36, 0.2);
    }
    .jb-badge {
        display: inline-block;
        background: #ef4444;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .jb-product-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 5px;
    }
    .jb-product-desc {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 10px;
    }
    .jb-product-price {
        font-size: 1.3rem;
        font-weight: 900;
        color: #fbbf24;
    }
    .jb-product-original-price {
        text-decoration: line-through;
        color: #64748b;
        font-size: 0.9rem;
        margin-left: 10px;
    }
    .jb-add-btn {
        width: 100%;
        padding: 12px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        border: none;
        border-radius: 8px;
        color: #0f172a;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        margin-top: 10px;
        transition: all 0.2s ease;
    }
    .jb-add-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.4);
    }
    .jb-cart-float {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 6px 20px rgba(251, 191, 36, 0.4);
        z-index: 1000;
        cursor: pointer;
    }
    .jb-section-title {
        font-size: 1.4rem;
        font-weight: 900;
        color: #fbbf24;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #334155;
    }
    .jb-combo-prompt {
        background: #334155;
        padding: 10px 15px;
        border-radius: 8px;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 15px;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Promo Banner
    st.markdown("""
    <div class="jb-promo-banner">
        <h3>🎉 30% OFF en tu primer pedido por la App</h3>
        <p>Usa el código: <strong>HOLAJUST</strong> | <a href="#" style="color:#0f172a;font-weight:700;">Descargar →</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for cart
    if 'jb_cart' not in st.session_state:
        st.session_state.jb_cart = []
    
    # Category selection
    categories = [
        "🍔 BURGER DEL MES!",
        "🔥 PROMOS EXCLUSIVAS",
        "⭐ Favoritas",
        "🍔 Especialidades",
        "🍗 Chicken",
        "👶 Kids",
        "🍟 Appetizers",
        "🥤 Para Tomar",
        "➕ Extras",
        "🍰 Postres",
        "🍺 Licores"
    ]
    
    selected_category = st.selectbox("Categoría", categories, index=0)
    
    # Product data by category
    products = {
        "🍔 BURGER DEL MES!": [
            {"name": "Burger del Mes", "desc": "Doble carne 180g, queso cheddar, bacon crocante, salsa especial de la casa", "price": 8990, "original": 11990, "badge": "-25%", "combo": True},
        ],
        "🔥 PROMOS EXCLUSIVAS": [
            {"name": "Promo Just Doble", "desc": "2 Burgers Clásicas + 2 Papas Medianas + 2 Bebidas", "price": 14990, "original": 19990, "badge": "-25%", "combo": False},
            {"name": "Promo Familiar", "desc": "4 Burgers a elección + 4 Papas + 4 Bebidas", "price": 27990, "original": 35990, "badge": "-22%", "combo": False},
            {"name": "Promo Pareja", "desc": "2 Burgers Especiales + 2 Papas + 2 Bebidas", "price": 16990, "original": 21990, "badge": "-23%", "combo": False},
        ],
        "⭐ Favoritas": [
            {"name": "Burger Clásica", "desc": "Carne 180g, queso cheddar, lechuga, tomate, salsa Just", "price": 6990, "original": None, "badge": None, "combo": True},
            {"name": "Burger Doble Queso", "desc": "Doble carne 360g, triple queso cheddar, bacon", "price": 9990, "original": None, "badge": "MÁS VENDIDA", "combo": True},
            {"name": "Burger BBQ Bacon", "desc": "Carne 180g, bacon, aros de cebolla, salsa BBQ", "price": 8490, "original": None, "badge": None, "combo": True},
        ],
        "🍔 Especialidades": [
            {"name": "Burger Trufada", "desc": "Carne Angus, queso brie, cebolla caramelizada, aceite de trufa", "price": 11990, "original": None, "badge": "PREMIUM", "combo": False},
            {"name": "Burger Blue Cheese", "desc": "Carne 180g, queso azul, nueces, rúcula, reducción de balsámico", "price": 10490, "original": None, "badge": None, "combo": False},
            {"name": "Burger Vegana", "desc": "Beyond Meat, queso vegano, palta, tomate seco", "price": 9990, "original": None, "badge": "NUEVA", "combo": False},
        ],
        "🍗 Chicken": [
            {"name": "Chicken Burger", "desc": "Pechuga crocante, lechuga, tomate, mayo", "price": 7490, "original": None, "badge": None, "combo": True},
            {"name": "Chicken Wings x6", "desc": "Alitas de pollo en salsa BBQ o Buffalo", "price": 6990, "original": None, "badge": None, "combo": False},
            {"name": "Nuggets x8", "desc": "Nuggets de pollo crocantes con salsa", "price": 4990, "original": None, "badge": None, "combo": False},
        ],
        "👶 Kids": [
            {"name": "Mini Burger Kids", "desc": "Mini burger + papas + jugo + juguete", "price": 5990, "original": None, "badge": None, "combo": False},
            {"name": "Chicken Nuggets Kids", "desc": "6 Nuggets + papas + jugo", "price": 4990, "original": None, "badge": None, "combo": False},
        ],
        "🍟 Appetizers": [
            {"name": "Papas Just", "desc": "Papas fritas crocantes con sal y especias", "price": 2990, "original": None, "badge": None, "combo": False},
            {"name": "Papas con Cheddar", "desc": "Papas + cheddar fundido + bacon", "price": 3990, "original": None, "badge": None, "combo": False},
            {"name": "Aros de Cebolla", "desc": "Aros de cebolla crocantes x8", "price": 3490, "original": None, "badge": None, "combo": False},
            {"name": "Tequeños x6", "desc": "Tequeños de queso con salsa de ajo", "price": 3990, "original": None, "badge": None, "combo": False},
        ],
        "🥤 Para Tomar": [
            {"name": "Bebida 500ml", "desc": "Coca-Cola, Sprite, Fanta", "price": 1990, "original": None, "badge": None, "combo": False},
            {"name": "Jugo Natural", "desc": "Naranja o Manzana 500ml", "price": 2490, "original": None, "badge": None, "combo": False},
            {"name": "Agua 500ml", "desc": "Con o sin gas", "price": 990, "original": None, "badge": None, "combo": False},
            {"name": "Milkshake", "desc": "Vainilla, Chocolate o Frutilla", "price": 3490, "original": None, "badge": None, "combo": False},
        ],
        "➕ Extras": [
            {"name": "Queso Extra", "desc": "Porción adicional de queso cheddar", "price": 990, "original": None, "badge": None, "combo": False},
            {"name": "Bacon Extra", "desc": "Tiras de bacon crocante", "price": 1490, "original": None, "badge": None, "combo": False},
            {"name": "Salsa Especial", "desc": "Salsa Just de la casa", "price": 490, "original": None, "badge": None, "combo": False},
        ],
        "🍰 Postres": [
            {"name": "Brownie", "desc": "Brownie de chocolate con helado", "price": 3490, "original": None, "badge": None, "combo": False},
            {"name": "Churros x4", "desc": "Churros rellenos de dulce de leche", "price": 2990, "original": None, "badge": None, "combo": False},
        ],
        "🍺 Licores": [
            {"name": "Cerveza Artesanal", "desc": "IPA o Golden Ale 500ml", "price": 3990, "original": None, "badge": None, "combo": False},
            {"name": "Cerveza Nacional", "desc": "Cristal, Kunstmann, Austral", "price": 2490, "original": None, "badge": None, "combo": False},
        ]
    }
    
    # Display products for selected category
    cat_key = selected_category
    if cat_key in products:
        for i, product in enumerate(products[cat_key]):
            # Combo prompt
            if product.get("combo"):
                st.markdown('<div class="jb-combo-prompt">💡 Hazla Combo agregando Fries + Bebida por $2,990</div>', unsafe_allow_html=True)
            
            # Product card
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if product.get("badge"):
                    badge_color = "#ef4444" if "%" in product["badge"] else "#fbbf24"
                    st.markdown(f'<span style="background:{badge_color};color:white;padding:3px 8px;border-radius:12px;font-size:0.75rem;font-weight:700;">{product["badge"]}</span>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="jb-product-name">{product["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="jb-product-desc">{product["desc"]}</div>', unsafe_allow_html=True)
                
                price_html = f'<span class="jb-product-price">${product["price"]:,}</span>'
                if product.get("original"):
                    price_html += f'<span class="jb-product-original-price">${product["original"]:,}</span>'
                st.markdown(price_html, unsafe_allow_html=True)
            
            with col2:
                if st.button("➕", key=f"add_{i}_{cat_key}", help=f"Agregar {product['name']}"):
                    st.session_state.jb_cart.append({**product, "qty": 1})
                    st.success("✅")
            
            st.markdown("---")
    
    # Cart Section
    if st.session_state.jb_cart:
        st.markdown('<div class="jb-section-title">🛒 Tu Carrito</div>', unsafe_allow_html=True)
        
        total = 0
        for i, item in enumerate(st.session_state.jb_cart):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['name']}**")
            with col2:
                st.write(f"${item['price']:,}")
            with col3:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.jb_cart.pop(i)
                    st.rerun()
            total += item['price']
        
        st.markdown("---")
        st.markdown(f"### Total: **${total:,}**")
        
        # Checkout buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💬 WhatsApp", type="primary"):
                items_text = "\n".join([f"• {item['name']}" for item in st.session_state.jb_cart])
                msg = f"🍔 Pedido Just Burger\n\n{items_text}\n\nTotal: ${total:,}"
                st.code(f"https://wa.me/56912345678?text={msg}", language=None)
        with col2:
            if st.button("✈️ Telegram", type="primary"):
                items_text = "\n".join([f"• {item['name']}" for item in st.session_state.jb_cart])
                msg = f"🍔 Pedido Just Burger\n\n{items_text}\n\nTotal: ${total:,}"
                st.code(f"https://t.me/SmarterChat_bot?text={msg}", language=None)
        with col3:
            if st.button("💳 Flow.cl", type="primary"):
                st.info("Redirigiendo a Flow.cl...")
