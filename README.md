# Action-Reaction

## Create an Automation Platform (similar to IFTTT / Zapier)

## 📌 Overview

Action-Reaction is an automation platform designed to connect services together.
Users can define **AREAs** (*Action + REAction*) that automatically execute when certain events occur.

The system is composed of three main parts:

- **Application Server**: Business logic & REST API.
- **Web Client**: Browser-based UI, communicates with the server.
- **Mobile Client**: Android app, communicates with the server.

---

## ✨ Features

- User registration & authentication (password-based + OAuth2).
- Service subscription (Google, Outlook, Dropbox, etc.).
- Action components (event triggers).
- REAction components (automated tasks).
- AREAs: link Actions to REActions.
- Hooks: monitor & trigger automation.

---

## 🏗 Architecture

- **Server**: Runs business logic, exposes REST API (`http://localhost:8080`).
- **Web Client**: User interface (`http://localhost:8081`).
- **Mobile Client**: Android application, distributed via APK.
- **Docker Compose**: Orchestration of all components.

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

WIP

### Services

- Server -> `http://localhost:8080/about.json`
- Web Client -> `http://localhost:8081/`
- Mobile Client APK -> YES

---

## 📜 API Example: `about.json`

WIP

---

## 🛠 Contributing

WIP

---

## 📅 Project Timeline

- **21/09/2025**: Tech stack selection, PoC, task distribution.
- **06/10/2025**: Core architecture & base functionality.
- **02/11/2025**: Full feature set, UI, Docker deployment.

---

## 📖 Documentation

WIP
