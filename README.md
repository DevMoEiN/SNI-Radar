<h1 align="center">📡 SNI Radar</h1>

<p align="center">
  <strong>An intelligent, high-speed SNI & CDN scanner featuring an advanced Dark Glassmorphism Web UI.</strong><br>
  <strong>اسکنر هوشمند و پرسرعت SNI و CDN با رابط کاربری وب مدرن (Glassmorphism)</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-black.svg" alt="Flask">
  <img src="https://img.shields.io/badge/UI-Glassmorphism-purple.svg" alt="UI Design">
</p>

<p align="center">
  👨‍💻 <b>Author (نویسنده):</b> <a href="https://t.me/itsthemoein">@itsthemoein</a> <br>
  📢 <b>Telegram Channel (کانال تلگرام):</b> <a href="https://t.me/PersiaTmChannel">@PersiaTmChannel</a>
</p>

---

## 🇺🇸 English

### ✨ Features
- **🎯 Intelligent Scanning:** Simultaneously checks Ping, TCP, SNI, and identifies CDN providers (Cloudflare, Vercel, Fastly, AWS, GCP, etc.).
- **⚡ High-Speed Concurrency:** Utilizes Python's `ThreadPoolExecutor` for blazing-fast multi-threaded scanning.
- **🎨 Modern Web UI:** Beautiful Dark Glassmorphism design with animated backgrounds and responsive layout.
- **📡 Live Streaming:** Real-time results streamed directly to the UI using NDJSON.
- **📊 Live Sorting:** Automatically sorts scan results based on network quality (Ping + TCP priority).
- **🛑 Total Control:** Fully adjustable thread speed, max CIDR host limits, and an instant "Stop" button.
- **🌐 Target Support:** Seamlessly handles individual IPs, Domains, and full CIDR subnets (e.g., `127.0.0.1/30`).

### 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DevMoEiN/SNI-Radar.git](https://github.com/DevMoEiN/SNI-Radar.git)
   cd SNI-Radar

    Install dependencies:
    Bash

    pip install flask

    Run the application:
    Bash

    python main.py

    The Web UI will automatically open in your default browser at http://127.0.0.1:10808.

📁 Custom Targets

Load default targets by creating a targets.txt file in the root directory. Add one IP, Domain, or CIDR per line.
🇮🇷 راهنمای فارسی
✨ امکانات

    🎯 اسکن هوشمند: بررسی هم‌زمان پینگ، TCP، SNI و تشخیص سرویس‌دهنده‌های CDN (کلودفلر، ورسل، آمازون و غیره).

    ⚡ سرعت بالا: استفاده از پردازش چندنخی (Multi-threading) برای اسکن فوق‌سریع.

    🎨 رابط کاربری مدرن: طراحی بسیار زیبای Dark Glassmorphism (شیشه‌ای تاریک) با پس‌زمینه متحرک و واکنش‌گرا.

    📡 پخش زنده (Live Stream): نمایش نتایج در لحظه روی مرورگر با استفاده از NDJSON.

    📊 مرتب‌سازی زنده: چیدمان خودکار نتایج بر اساس کیفیت و در دسترس بودن شبکه (اولویت با اتصال TCP و Ping).

    🛑 کنترل کامل: قابلیت تنظیم سرعت اسکن (تعداد تردها)، سقف هاست‌های CIDR و دکمه توقف فوری اسکن.

    🌐 پشتیبانی از اهداف مختلف: امکان اسکن IP، دامنه (رنج‌ها) و ساب‌نت‌های CIDR (مثلاً 127.0.0.1/30).

🚀 آموزش نصب و استفاده

۱. دریافت سورس‌کد:
Bash

git clone [https://github.com/DevMoEiN/SNI-Radar.git](https://github.com/DevMoEiN/SNI-Radar.git)
cd SNI-Radar

۲. نصب پیش‌نیازها:
این ابزار به فریم‌ورک Flask نیاز دارد:
Bash

pip install flask

۳. اجرای برنامه:
Bash

python main.py

پس از اجرا، رابط کاربری وب به‌صورت خودکار در آدرس http://127.0.0.1:10808 مرورگر شما باز می‌شود.
