<!-- SECURITY.md -->

# 🔐 Security Policy

---

## 📦 Supported Versions

Security updates are provided for:

| Version | Supported |
|--------|----------|
| Latest | ✅ |
| >= 1.0.0 | ✅ |
| < 1.0.0 | ❌ |

Older versions may contain known vulnerabilities and are not supported.

---

## 🚨 Reporting a Vulnerability

If you find a security issue:

1. Please **Do NOT open a public issue for security vulnerabilities**
2. Report privately to the maintainer

Include:

- description
- reproduction steps
- impact
- possible fix

---

## 🔍 Security Scope

This project is a CLI tool. Relevant risks include:

- malicious file paths
- directory traversal issues
- unsafe file writes
- command injection via CLI input

---

## 🛡️ Mitigation Guidelines

- validate inputs
- avoid executing user input
- sanitize file paths
- use safe file operations

---

## ⚡ Response Policy

The maintainer will:

- investigate
- confirm issue
- release fix if needed