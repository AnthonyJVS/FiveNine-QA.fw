# QA Automation Framework

End-to-end test automation framework for web applications, covering **UI** and **API** layers.  
Built with **Python** · **Playwright** · **pytest**.

**Target:** [automationexercise.com](https://automationexercise.com) — an e-commerce platform with a full UI and REST API.

---

## 🚀 Key Features

- **~40 UI tests** — login, registration, navigation, product search, cart, contact form
- **~25 API tests** — products, brands, search, auth, user CRUD
- **Smoke suite** — critical-path checks that run in under a minute
- **Page Object Model** — clean separation between test logic and page interaction
- **Streamlit dashboard** — run tests and view results from a web UI
- **GitHub Actions CI** — automated pipeline with smoke → API → UI stages
- **Docker support** — one-command test execution in a container
- **Allure + HTML reports** — two reporting options, zero manual setup

---

## 🛠 Tech Stack

### Core
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Pytest](https://img.shields.io/badge/pytest-Test%20Runner-green?style=for-the-badge&logo=pytest)
![Playwright](https://img.shields.io/badge/Playwright-Browser%20Automation-2EAD33?style=for-the-badge&logo=playwright)

### API & Data
![Requests](https://img.shields.io/badge/requests-API%20Testing-darkred?style=for-the-badge)
![Faker](https://img.shields.io/badge/Faker-Test%20Data-purple?style=for-the-badge)
![dotenv](https://img.shields.io/badge/python--dotenv-Config-grey?style=for-the-badge)

### Reporting & CI
![Allure](https://img.shields.io/badge/Allure-Reports-orange?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-black?style=for-the-badge&logo=githubactions)
![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=for-the-badge&logo=docker)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)

---

## ⚡ Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/yourusername/FiveNine-QA.fw
cd FiveNine-QA.fw

python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
playwright install --with-deps chromium
```

### 2. (Optional) Adjust settings

The framework reads its config from `.env` files inside `config/environments/`.  
Three profiles ship by default: `dev`, `staging`, `prod`.

```bash
# Switch environment (Linux/macOS)
export ENV=staging 

# Switch environment (Windows PowerShell)
$env:ENV="staging"

# Switch environment (Windows CMD)
set ENV=staging
```

---

## ⚙️ Configuration

Core settings you can tweak in your `.env` or project config:

- **`BASE_URL`** — target application URL (default: `https://automationexercise.com`)
- **`BROWSER`** — browser engine: `chromium`, `firefox`, or `webkit`
- **`HEADLESS`** — set to `false` to watch the browser in headed mode
- **`SLOW_MO`** — delay between actions in milliseconds (useful for debugging)
- **`DEFAULT_TIMEOUT`** — interaction timeout in milliseconds

---

## 🧪 Running Tests

All commands assume you're in the project root with the virtualenv active.

### The basics

```bash
# Run all tests
pytest

# Run only smoke tests
pytest -m smoke

# Run only UI tests
pytest tests/ui/ -v

# Run only API tests
pytest tests/api/ -v
```

### Run by Feature

```bash
pytest -m login
pytest -m registration
pytest -m search
pytest -m cart
pytest -m contact
pytest -m negative      # edge cases and error paths
```

### Available Markers

| Marker | Description |
| :--- | :--- |
| `smoke` | Fast CI sanity checks |
| `regression` | Full regression suite |
| `ui` | All browser-based tests |
| `api` | API-only tests (no browser) |
| `login` | Authentication tests |
| `registration` | Signup / account creation tests |
| `navigation` | Page loading and navigation tests |
| `search` | Product search tests |
| `cart` | Shopping cart tests |
| `contact` | Contact form tests |
| `negative` | Negative / error-path scenarios |

---

## 📊 Reports

### HTML Report (Auto-generated)

Every test run produces `reports/report.html` — a self-contained file you can open in any browser.

```bash
# Windows
start reports/report.html

# macOS
open reports/report.html

# Linux
xdg-open reports/report.html
```

### Other Artifacts

| Folder | Content |
| :--- | :--- |
| `reports/` | HTML reports |
| `screenshots/` | Auto-captured on test failure |
| `logs/` | Timestamped execution logs |
| `allure-results/` | Raw Allure data |

---

## 🖥 Streamlit Dashboard

A web interface for running tests and browsing results — no terminal required.

```bash
pip install -r requirements-dashboard.txt
streamlit run dashboard/app.py
```

Features:
- Pick a test suite (`smoke` / `api` / `ui` / `all`)
- Choose a browser and headless/headed mode
- Run tests and see output in real time
- Browse HTML reports, failure screenshots, and logs

---

## 🔗 CI/CD — GitHub Actions

The pipeline (`.github/workflows/ci.yml`) triggers on every push to `main`/`develop` and on pull requests.

- **Artifacts**: Reports and screenshots are kept for 14 days.
- **Auto-cancel**: Concurrent runs on the same branch auto-cancel to save resources.
- **Manual Control**: dispatch via `workflow_dispatch` with custom parameters.

---

## 🐳 Docker

Run tests inside a container without needing a local browser installation.

```bash
# Full suite
docker compose up tests

# Smoke only
docker compose up smoke-tests

# API only
docker compose up api-tests

# Rebuild after changes
docker compose build --no-cache && docker compose up tests
```

---

## 📄 License

This project is built for educational and portfolio purposes.
