# QA Automation Framework

End-to-end test automation framework for web applications, covering **UI** and **API** layers.  
Built with Python · Playwright · pytest.

**Target:** [automationexercise.com](https://automationexercise.com) — an e-commerce platform with a full UI and REST API.

---

## What's inside

- **~40 UI tests** — login, registration, navigation, product search, cart, contact form
- **~25 API tests** — products, brands, search, auth, user CRUD
- **Smoke suite** — critical-path checks that run in under a minute
- **Page Object Model** — clean separation between test logic and page interaction
- **Streamlit dashboard** — run tests and view results from a web UI
- **GitHub Actions CI** — automated pipeline with smoke → API → UI stages
- **Docker support** — one-command test execution in a container
- **Allure + HTML reports** — two reporting options, zero manual setup

---

## Tech Stack

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

## Quick start

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
# Switch environment
set ENV=staging    # Windows
export ENV=staging # macOS / Linux
```

## Configuration

Core settings you may want to tweak before running the framework:

- **`BASE_URL`** — target application URL, default: `https://automationexercise.com`
- **`BROWSER`** — browser engine: `chromium`, `firefox`, or `webkit`
- **`HEADLESS`** — set to `false` if you want to watch the browser
- **`SLOW_MO`** — adds delay between actions in milliseconds, useful for debugging
- **`DEFAULT_TIMEOUT`** — default element interaction timeout in milliseconds
---

## Running tests

All commands assume you're in the project root with the virtualenv active.

### The basics

```bash
# Everything
pytest

# Only smoke tests
pytest -m smoke

# Only UI tests
pytest tests/ui/ -v

# Only API tests
pytest tests/api/ -v
```

### By feature

```bash
pytest -m login
pytest -m registration
pytest -m search
pytest -m cart
pytest -m contact
pytest -m negative      # edge cases and error paths
```

### Debug mode

```bash
# Headed browser + slow motion
HEADLESS=false pytest tests/ui/test_login.py -v --slow-mo=500

# More verbose output
pytest -v --tb=long -s
```

### Available markers

 `smoke`         Fast CI sanity checks              
 `regression`    Full regression suite              
 `ui`            All browser-based tests            
 `api`           API-only tests (no browser)        
 `login`         Authentication tests               
 `registration`  Signup / account creation tests    
 `navigation`    Page loading and navigation tests  
 `search`        Product search tests               
 `cart`          Shopping cart tests                 
 `contact`       Contact form tests                 
 `negative`      Negative / error-path scenarios    

---

## Reports

### HTML report (auto-generated)

Every test run produces `reports/report.html` — a self-contained file you can open in any browser.

```bash
# Windows
start reports/report.html

# macOS
open reports/report.html

# Linux
xdg-open reports/report.html
```

### Other artifacts

| Folder            | Content                                        |
|-------------------|-------------------------------------------------|
| `reports/`        | HTML reports                                    |
| `screenshots/`    | Auto-captured on test failure                   |
| `logs/`           | Timestamped execution logs                      |
| `allure-results/` | Raw Allure data                                 |

---

## Streamlit dashboard

A web interface for running tests and browsing results — no terminal required.

```bash
pip install -r requirements-dashboard.txt
streamlit run dashboard/app.py
```

From the dashboard you can:

- Pick a test suite (`smoke` / `api` / `ui` / `all`)
- Choose a browser and headless/headed mode
- Run tests and see output in real time
- Browse HTML reports, failure screenshots, and logs

---

## CI/CD — GitHub Actions

The pipeline (`.github/workflows/ci.yml`) triggers on every push to `main` / `develop` and on pull requests.

```
Push / PR
  │
  ├── 🔥 Smoke Tests     ─── fast sanity check
  ├── 🌐 API Tests        ─── API endpoint validation
  │
  └── (smoke passes)
        └── 🖥️ UI Tests   ─── full browser regression
              │
              └── 📊 Summary ─── aggregate results
```

- Reports and screenshots are uploaded as **GitHub Actions artifacts** (kept 14 days).
- Concurrent runs on the same branch auto-cancel to save minutes.
- Manual dispatch via `workflow_dispatch` with a `test_suite` input.

---

## Docker

Run everything inside a container — no local browser install needed.

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

Reports, screenshots, and logs are mounted back to your host.

---

## Project structure

```
├── .github/workflows/ci.yml     # CI pipeline
├── config/
│   ├── settings.py              # Typed settings (dataclass)
│   └── environments/            # .env.dev, .env.staging, .env.prod
├── pages/                       # Page Object Model
│   ├── base_page.py             # Shared helpers (click, fill, wait, navigate)
│   ├── home_page.py
│   ├── login_page.py
│   ├── registration_page.py
│   ├── products_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   └── contact_page.py
├── tests/
│   ├── conftest.py              # Browser lifecycle fixtures
│   ├── ui/                      # 7 UI test files
│   │   └── conftest.py          # Page object injection
│   └── api/                     # 5 API test files
│       └── conftest.py          # API client fixture
├── utils/
│   ├── api_client.py            # HTTP client wrapper (requests)
│   ├── logger.py                # File + console logger
│   ├── helpers.py               # Screenshots, retry, timestamps
│   └── fake_data.py             # Faker-based data generators
├── test_data/                   # Static payloads (JSON)
├── dashboard/app.py             # Streamlit dashboard
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dashboard.txt
├── pytest.ini
└── ROADMAP.md
```

---

## Architecture at a glance

```
Tests (ui / api / smoke)
  │
  ▼
Fixtures (conftest.py per layer)
  │
  ▼
Page Objects (BasePage → concrete pages)     API Client (requests wrapper)
  │                                              │
  ▼                                              ▼
Playwright browser                           automationexercise.com/api
  │
  ▼
automationexercise.com
```

**Why this structure?**

- **Page Object Model** — selector changes stay isolated in one file; tests stay readable.
- **Fixture injection** — browser, context, page objects, and API client are all managed by pytest fixtures. Tests don't create or tear down anything manually.
- **Environment configs** — switch between `dev` / `staging` / `prod` with a single env var. No hardcoded URLs.
- **Dynamic test data** — Faker generates unique names, emails, and passwords per run, so tests never collide.
- **Session-scoped browser** — the browser starts once per test session (performance), but each test gets its own context (isolation).

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) — includes planned features like cross-browser CI matrix, parallel execution, visual regression, and BDD integration.

---

## License

This project is built for educational and portfolio purposes.
