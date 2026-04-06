# ──────────────────────────────────────────────
# QA Automation Framework — Docker Image
# ──────────────────────────────────────────────
# Uses the official Playwright Python image which includes
# all browser dependencies pre-installed.

FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV=staging \
    HEADLESS=true \
    BROWSER=chromium

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy project files
COPY . .

# Create artifact directories
RUN mkdir -p reports screenshots logs allure-results

# Default command: run all tests
CMD ["pytest", "tests/", "-v", \
     "--html=reports/report.html", \
     "--self-contained-html", \
     "--alluredir=allure-results"]
