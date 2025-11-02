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

- **Step 1**: Connect your phone with your laptop via a cable
- **Step 2**: docker-compose build && docker-compose up
- **Step 3**: Go to your browser -> connect to http://localhost:8081/ to be at the web interface
- **Step 4**:Connect to http://localhost:8081/client.apk to download the mobile app

### Services

- Server -> `http://localhost:8080/about.json`
- Web Client -> `http://localhost:8081/`
- Mobile Client APK -> YES

---

## 📜 API Example: `about.json`

WIP

---

## 🛠 Contributing

### Languages and framework

- Web App: React + SCSS
- Mobile App: React + Capacitor + SCSS
- Server: Python + fastapi

### How to add a service

-> Go to area/back/app/routes
-> Add a folder and name it after the service you want to add
-> Create a `__init__.py` file following other examples
-> Create the .py file for the service and complete it following the other examples

### How to add an A-REA

WIP

---

## 📅 Project Timeline

- **21/09/2025**: Tech stack selection, PoC, task distribution.
- **06/10/2025**: Core architecture & base functionality.
- **02/11/2025**: Full feature set, UI, Docker deployment.

---

## 📖 Documentation

WIP
