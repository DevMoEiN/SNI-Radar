<h1 align="center">📡 SNI Radar</h1>

<p align="center">
  <strong>An intelligent, high-speed SNI & CDN scanner featuring an advanced Dark Glassmorphism Web UI.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-black.svg" alt="Flask">
  <img src="https://img.shields.io/badge/UI-Glassmorphism-purple.svg" alt="UI Design">
  <img src="https://img.shields.io/badge/Threads-Concurrent-green.svg" alt="Concurrency">
</p>

---

## ✨ Features

- **🎯 Intelligent Scanning:** Simultaneously checks Ping, TCP, SNI, and identifies CDN providers (Cloudflare, Vercel, Fastly, AWS, GCP, etc.).
- **⚡ High-Speed Concurrency:** Utilizes Python's `ThreadPoolExecutor` for blazing-fast multi-threaded scanning.
- **🎨 Modern Web UI:** Beautiful Dark Glassmorphism design with animated backgrounds and responsive layout.
- **📡 Live Streaming:** Real-time results streamed directly to the UI using NDJSON.
- **📊 Live Sorting:** Automatically sorts scan results based on network quality (Ping + TCP priority).
- **🛑 Total Control:** Fully adjustable thread speed, max CIDR host limits, and an instant "Stop" button.
- **🌐 Target Support:** Seamlessly handles individual IPs, Domains, and full CIDR subnets (e.g., `127.0.0.1/30`).

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/SNI-Radar.git](https://github.com/YOUR_USERNAME/SNI-Radar.git)
   cd SNI-Radar
