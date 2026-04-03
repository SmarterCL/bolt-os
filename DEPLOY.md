# 🦞 BOLT OS - Deployment Guide

**URL:** https://share.streamlit.io/new/deploy-from-template/b8e65aff-d8c7-4b7d-9d4c-eb79249dfc4b

---

## 🚀 Deploy to Streamlit Cloud

### Step 1: Connect Repository

1. Go to: https://share.streamlit.io/new/deploy-from-template/b8e65aff-d8c7-4b7d-9d4c-eb79249dfc4b
2. Connect your GitHub account
3. Select repository: `SmarterCL/bolt-os`
4. Branch: `main`
5. Main file: `app.py`

### Step 2: Set Environment Variables

In Streamlit Cloud settings, add:

```
API_URL=http://89.116.23.167:8002
WEBHOOK_URL=http://89.116.23.167:8003
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID=6683244662
```

### Step 3: Deploy

Click "Deploy!" and wait for the app to start.

---

## 📊 Features

### 1. 📊 Status Tab
- System health check
- Service status (API, Webhook, Telegram)
- Real-time metrics

### 2. 🧪 Events Tab
- Manual event injection
- Stress test runner (10-100 events)
- Real-time results visualization

### 3. 🔴 Live Logs Tab
- Last 100 log entries
- Filter by status (VALID, SANDBOX, REJECTED)
- Auto-refresh every N seconds

### 4. 📈 Metrics Pro Tab
- Total events, valid/sandbox/reject rates
- Status distribution pie chart
- Score distribution histogram
- Price vs Score scatter plot
- Policy engine indicators
- Automatic policy actions

### 5. 🤖 Bot Control Tab
- Send Telegram messages
- Configure automatic alerts
- View recent alerts

### 6. 💰 Revenue Tab
- Revenue estimation
- Revenue breakdown chart
- Monthly projection

---

## 🔗 Architecture

```
Users → Bots (Telegram/WhatsApp)
        ↓
      API (VPS)
        ↓
   Postgres + Redis
        ↓
 Policy Engine
        ↓
     Actions
        ↓
  BOLT OS (Streamlit UI)
        ↓
 Control + Observability
```

---

## 📁 Files

```
bolt-streamlit/
├── app.py                    ← Main Streamlit app
├── requirements.txt          ← Python dependencies
└── .streamlit/
    └── config.toml           ← Streamlit configuration
```

---

## 🎯 Usage

### Manual Event
1. Go to "🧪 Eventos" tab
2. Select product, enter price/quantity
3. Click "🚀 Enviar Evento"
4. View real-time result

### Stress Test
1. Go to "🧪 Eventos" tab
2. Set number of events (10-100)
3. Click "🧪 Ejecutar Stress Test"
4. View distribution chart

### Live Logs
1. Go to "🔴 Logs" tab
2. Select filter (optional)
3. Click "🔄 Refresh" or wait for auto-refresh

### Metrics Pro
1. Go to "📈 Metrics Pro" tab
2. View all charts and indicators
3. Monitor policy engine actions

### Bot Control
1. Go to "🤖 Bot Control" tab
2. Enter message and chat ID
3. Click "📤 Enviar a Telegram"

### Revenue
1. Go to "💰 Revenue" tab
2. View revenue breakdown
3. Check monthly projection

---

## 🔧 Troubleshooting

### API Offline
- Check VPS is running: `ssh root@89.116.23.167`
- Verify API service: `systemctl status smarter-food`
- Check port: `curl http://localhost:8002/health`

### No Logs
- Check log directory exists: `/var/log/smarter/`
- Verify log file: `/var/log/smarter/events.log`
- Check permissions: `ls -la /var/log/smarter/`

### Telegram Not Sending
- Verify bot token is correct
- Check chat ID is valid
- Test manually: `curl https://api.telegram.org/bot<TOKEN>/getMe`

---

**🦞 BOLT OS v1.0 - SmarterOS Control Panel 24x7**
