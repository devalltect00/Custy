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
ENV CUSTY_CONTAINER=1

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
    micro \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Custy's container-only editor shortcuts. Local editor configuration remains
# owned by the host user and is not modified by the image.
COPY docker/editors /etc/custy/editors

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

ARG CUSTY_BUILD_VERSION=0.1.0

# =========================
# 📦 Install DEV dependencies
# =========================

RUN SETUPTOOLS_SCM_PRETEND_VERSION_FOR_CUSTY="${CUSTY_BUILD_VERSION}" \
    pip install --no-cache-dir -e ".[dev]"

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

ARG CUSTY_BUILD_VERSION=0.1.0

# =========================
# 📦 INSTALL RUNTIME DEPENDENCIES
# =========================

RUN SETUPTOOLS_SCM_PRETEND_VERSION_FOR_CUSTY="${CUSTY_BUILD_VERSION}" \
    pip install --no-cache-dir .

# Fail the image build when a runtime import or CLI startup dependency is
# missing without depending on command-specific exit-code behavior.
RUN python -c "from app.cli.main import app"

# =========================
# 🚀 Default command
# =========================

ENTRYPOINT ["custy"]

CMD ["--help"]
