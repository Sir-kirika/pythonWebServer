# FastAPI WebSocket Dashboard for MT5 DLL

## Overview

This project demonstrates a **real-time WebSocket-based dashboard** for MetaTrader 5 (MT5) using a custom DLL, Python FastAPI server, and browser client. It allows an MT5 DLL to push live data (signals, metrics, or computed results) to a web page in real time.

Key features:

- MT5 DLL sends JSON data to the FastAPI server over **WSS** (secure WebSocket).  
- Python FastAPI server broadcasts the data to **all connected web clients**.  
- Browser client displays live updates without refreshing.  
- Supports multiple DLL instances and multiple web clients simultaneously.  
- Optional local SSL certificate for development, with recommendations for trusted CA certs in production.  

---

## Project Components

### 1. MT5 DLL
- Acts as a WebSocket client, pushing JSON-formatted data to the server.  
- Requires a token for authentication (`supersecret123` by default).  
- Example JSON structure:
```json
{
   "key": "EA1",
   "src": "EURUSD_PERIOD_H1",
   "clientId": "EA1_123456",
   "data": [
      {"pair":"EURUSD","TF_data":[{"M1":1.2,"cell_color":"clrGreen"}],"sum":1.2,"sum_cell_color":"clrGreen"}
   ]
}
```

### 2. FastAPI Server
- Handles two types of connections:  
  1. DLLs connecting with a token (push data)  
  2. Web clients connecting to receive live updates  
- Can run **secure (WSS)** and **insecure (WS)** endpoints simultaneously.  
- Broadcasts incoming DLL data to all connected web clients.  

### 3. Web Client (HTML/JS)
- Connects to the server via WebSocket (WS/WSS).  
- Receives and displays live data pushed from DLLs.  
- Automatically reconnects if connection is lost.  
- Minimal UI for demonstration; customizable as needed.  

---

## Deployment Instructions

### 1. Local Development
- Use self-signed certs:
```bash
openssl req -x509 -newkey rsa:4096 -keyout local.key -out local.crt -days 365 -nodes -subj "/CN=localhost"
```
- Start server:
```bash
python server.py
```
- Web clients connect to `ws://localhost:8000/ws` (insecure) for testing.  

### 2. Production Deployment
- Use **trusted SSL certificates** (Let’s Encrypt or commercial CA).  
- Run server behind a **reverse proxy** (NGINX/Caddy) for WSS.  
- Use a **production ASGI server** like Gunicorn with Uvicorn workers:
```bash
gunicorn -k uvicorn.workers.UvicornWorker server:app -b 0.0.0.0:443 --certfile=/path/to/fullchain.pem --keyfile=/path/to/privkey.pem --workers 4
```
- Consider running the server as a **systemd service** on Linux or a scheduled task/service on Windows for continuous uptime.  

---

## Limits and Recommendations

- **DLL Security**: Keep the token secret. Rotate periodically for production.  
- **Concurrent Clients**: Tested with multiple DLLs and web clients; each new connection increases memory usage. Consider connection limits if high volume.  
- **Data Size**: JSON payloads should remain moderate (<1 MB) to prevent blocking the event loop.  
- **SSL**: For live deployment, always use trusted certificates to prevent handshake errors.  
- **Error Handling**: Server cleans up dead client connections automatically.  

---

## Folder Structure

```
project/
├─ server.py            # FastAPI WebSocket server
├─ local.key            # Local dev SSL key (optional)
├─ local.crt            # Local dev SSL cert (optional)
├─ index.html           # Web client dashboard
├─ README.md            # This document
└─ mt5_dll/             # Placeholder for MT5 DLL files
```

---

## Usage Summary

1. **Compile DLL** for MT5 with WebSocket support.  
2. **Start FastAPI server** on your host/VPS.  
3. **Connect web clients** to receive live updates.  
4. **Push data from DLL** and verify real-time display on the dashboard.  

---

## Contributions

- Fork the repo, modify server or web client, and submit pull requests.  
- Suggestions welcome for better dashboard UI, authentication, and scalability.  

---

## Architecture Diagram (Optional)

```
MT5 DLL --> [ FastAPI Server (WSS/WS) ] --> Web Browser Clients
```

