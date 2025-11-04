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

 - **Step 1**: Go to back and a create a \`config.toml\` file. Fill it based on the data in exemples/exemple_config:
    The `jwt_secret` is an ascii string.
    For each routes fill the `client_id` and `client_secret` with your own.
    Note for caldav/gmail/youtube, use the same `client_id`/`client_secret`. The `client_id` must finish with `.apps.googleusercontent.com`.

 In the provider section, replace the client_id and client_secret with your client_id and client_secret. Repeat for every provider. (They can be found in back/app/routes)

- **Step 2**: Go to front and create a \`gradle.properties\` file. Fill it with the informations in exemples/exemple_gradle. Fill `RELEASE_STORE_PASSWORD` and `RELEASE_KEY_PASSWORD` with your own password. The two must have an identical one.

- **Step 3**: In your terminal run `keytool -genkey -v -keystore apk_key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias alias;`.
It will ask for a keystore password, put the one you chose for the second step. It will follow by asking more information; those information don't need to be necesarilly true.
Enter 'y' to confirm the datas you entered.

- **Step 4**: Run `docker compose up --build`


### Services

- Server -> `http://localhost:8080/about.json`
- Web Client -> `http://localhost:8081/`
- Mobile Client APK -> YES

---

## 📜 API Example: `about.json`

WIP

---

## 📅 Project Timeline

- **21/09/2025**: Tech stack selection, PoC, task distribution.
- **06/10/2025**: Core architecture & base functionality.
- **02/11/2025**: Full feature set, UI, Docker deployment.

---

## 📖 Documentation

- **API**: http://localhost:8080/docs
