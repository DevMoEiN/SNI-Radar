# 🚀 SNI Radar

> 🔍 Intelligent SNI / TCP / Ping / CDN Scanner with Live Streaming UI
> 🔍 اسکنر هوشمند SNI / TCP / پینگ / CDN با رابط گرافیکی زنده

---

## ✨ Features | ویژگی‌ها

* ⚡ Live Streaming Results (NDJSON)
  ⚡ نمایش نتایج به‌صورت زنده

* 🧠 Smart SNI Detection
  🧠 تشخیص هوشمند SNI

* 🌐 CDN Provider Identification
  🌐 شناسایی ارائه‌دهنده CDN

* 📡 Ping + TCP Health Checks
  📡 بررسی پینگ و اتصال TCP

* 🧵 Multi-threaded Scanning (1–100 threads)
  🧵 اسکن چند نخی (۱ تا ۱۰۰ ترد)

* 🛑 Real-time Stop Control
  🛑 توقف آنی اسکن

* 🎯 CIDR Expansion Support
  🎯 پشتیبانی از CIDR

* 🎨 Modern Glassmorphism UI
  🎨 رابط کاربری مدرن گلس

* 📊 Live Metrics Dashboard
  📊 داشبورد آمار لحظه‌ای

* 💾 Auto-save JSON Results
  💾 ذخیره خودکار نتایج

---

## 🧠 What is this? | این ابزار چیه؟

**SNI Radar** یک ابزار قدرتمند برای تحلیل شبکه است که موارد زیر را بررسی می‌کند:

* Domain / IP / CIDR
* TLS SNI usability
* CDN detection
* Network reachability

📌 مناسب برای:

* تست بای‌پس
* تحلیل CDN
* دیباگ شبکه
* تحقیقات امنیتی

---

## ⚙️ Installation | نصب

```bash
git clone https://github.com/DevMoEiN/SNI-Radar.git
cd SNI-Radar
pip install flask
```

---

## ▶️ Run | اجرا

```bash
python sni_web.py
```

سپس باز کن:

```
http://127.0.0.1:10808
```

---

## 📥 Input Examples | مثال ورودی

```
cloudflare.com
1.1.1.1
8.8.8.8
127.0.0.1/30
```

---

## 📊 Output | خروجی

| Target      | IP        | Ping | TCP | SNI | CDN        | Status     |
| ----------- | --------- | ---- | --- | --- | ---------- | ---------- |
| example.com | 104.x.x.x | 32ms | ✅   | ✅   | Cloudflare | SNI-USABLE |

---

## 🧩 How It Works | نحوه کار

1. Resolve domain → IP
2. Ping test
3. TCP connection
4. TLS (SNI) handshake
5. CDN detection
6. Final scoring

---

## 📁 Output Files | فایل خروجی

بعد از هر اسکن:

```
sni_results_YYYYMMDD_HHMMSS.json
```

---

## 🛠️ Tech Stack

* Python 🐍
* Flask 🌐
* ThreadPoolExecutor ⚡
* Vanilla JS 🎨

---

## 📡 API

### `POST /api/scan`

```json
{
  "targets": ["example.com"],
  "strict_ping": true,
  "max_hosts": 4096,
  "threads": 10
}
```

### `POST /api/stop`

Stop current scan
توقف اسکن

---

## ⚠️ Disclaimer | هشدار

This project is for **educational purposes only**.
از این ابزار فقط برای اهداف آموزشی استفاده کنید.

---

## 👤 Author | سازنده

* Telegram: **@itsthemoein**

---

## 📢 Channel | کانال

* Telegram: **@persiatmchannel**

---

## ⭐ Support

اگر خوشت اومد:

* ⭐ Star کن
* 🍴 Fork کن
* 💡 ایده بده

---

## 🔥 Future Plans

* GeoIP 🌍
* CSV / HTML export 📄
* WebSocket mode ⚡
* Docker 🐳
* Themes 🎨

---

> Made with ❤️ by Moein
