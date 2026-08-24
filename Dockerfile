# Dockerfile

# =========================================================
# ➤ BASE STAGE
# =========================================================

# =========================
# 💿 Base image
# =========================

# Use official Python image
FROM python:3.14-slim AS base

# =========================
# 🔡 Environment
# =========================

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# 📁 Working directory (WORKSPACE)
# =========================

# Set working directory
WORKDIR /workspace

# =========================
# 📦 SYSTEM DEPENDENCIES
# =========================

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

# NOTE:
# Don't use like these below when install
#   make \
#   git \
#   # docker.io \
#   # docker-cli \
#   docker-ce-cli \
# Comments inside a \ continuation can produce unexpected parsing behavior.

# =========================
# 📄 Copy application
# =========================

COPY . .

# =========================
# 🚀 PYTHON SETUP
# =========================

RUN pip install --no-cache-dir --upgrade pip


# =========================================================
# ➤ DEVELOPMENT STAGE
# =========================================================

# =========================
# 💿 DEVELOPMENT IMAGE
# =========================

FROM base AS development

# =========================
# 📦 Install DEV dependencies
# =========================

RUN pip install --no-cache-dir -e ".[dev]"

# =========================
# 🚀 Default command
# =========================

ENTRYPOINT ["custy"]

CMD ["--help"]


# =========================================================
# ➤ PRODUCTION STAGE
# =========================================================

# =========================
# 💿 PRODUCTION IMAGE
# =========================

FROM base AS production

# =========================
# 📦 INSTALL RUNTIME DEPENDENCIES
# =========================

RUN pip install --no-cache-dir .

# Fail the image build when a runtime import or CLI startup dependency is
# missing without depending on command-specific exit-code behavior.
RUN python -c "from app.cli.main import app"

# =========================
# 🚀 Default command
# =========================

ENTRYPOINT ["custy"]

CMD ["--help"]
