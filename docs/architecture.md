# Architecture

## Overview

This project demonstrates an AI-assisted installer automation system for malware analysis research.

The system is divided into three parts:

1. Dropper (User Machine)
2. Sandbox Execution Environment
3. AI Analysis Server

---

# 1. Dropper (User Machine)

The dropper is responsible for:

- Downloading the installer sample
- Downloading the automation client
- Launching the installer
- Starting the AI automation process

Files:
- client/dropper.py

---

# 2. Sandbox Environment

The installer executes inside a sandbox environment such as ANY.RUN.

The automation client runs inside the sandbox and:

- Detects installer windows
- Captures screenshots
- Sends screenshots to the AI server
- Receives predicted actions
- Clicks installer buttons automatically

Files:
- client/ai_clicker.py

---

# 3. AI Analysis Server

The AI server processes screenshots received from the sandbox.

The server uses:
- CLIP Vision Transformer (ViT-B/32)
- OCR-based text extraction
- Rule-based installer action classification

The server predicts actions such as:
- Next
- Install
- Accept Agreement
- Finish

Files:
- server/ai_server.py

---

# Workflow

1. User executes dropper
2. Installer launches in sandbox
3. Automation client captures installer screenshots
4. Screenshots sent to AI server
5. AI server predicts next action
6. Client performs UI interaction automatically
7. Installation completes

---

# AI Components

## Visual Transformer

The project uses OpenAI CLIP ViT-B/32 for visual understanding of installer screens.

Capabilities:
- Screen classification
- Button context understanding
- Installer state prediction

---

# OCR Layer

Tesseract OCR is used for:
- Extracting installer text
- Agreement detection
- Button identification

---

# Safety Note

This project is developed strictly for:
- Malware analysis research
- Automated sandbox testing
- Academic experimentation

No persistence, privilege escalation, or malicious payloads are included.