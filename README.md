# 🚀 BPI Monitor & Automation Tracker

![CI/CD Pipeline](https://github.com/yourusername/repo/actions/workflows/ci.yml/badge.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)

An enterprise-grade automation system that tracks the Bitcoin Price Index (BPI) via the Coinbase API, generates rich visualizations (Line & Candlestick charts), and produces a beautiful HTML dashboard alongside automated email alerts.

## 🏗️ Architecture

```mermaid
graph TD
    A[main.py / Entry Point] --> B(Business Logic)
    B --> C[API Client - Coinbase]
    B --> D[Storage - JSON]
    B --> E[Visualizer - Pandas/Matplotlib]
    B --> F[Notifier - SMTP Email]
    E --> G((HTML Dashboard))
    E --> H((Candlestick Chart))
    E --> I((Line Chart))
```

## ⚙️ Installation & Usage

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up Environment Variables:**
   Copy `.env.example` to `.env` and fill in necessary details (e.g. SMTP settings).
4. **Run the tracker:**
   ```bash
   python main.py
   ```