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
- **Step 2**: docker build -t test -f android/Dockerfile . && docker run test:latest
- **Step 3**: Go to your browser -> connect to http://localhost:8081/ to be at the web interface
- **Step 4**: Connect to http://localhost:8081/client.apk to download the mobile app

#### Mobile installation

- **Step 1**: Go to front/android and create a \`gradle.properties\` file. Fill it with those informations:

\# Project-wide Gradle settings.

\# IDE (e.g. Android Studio) users:
\# Gradle settings configured through the IDE *will override*
\# any settings specified in this file.

\# For more details on how to configure your build environment visit
\# http://www.gradle.org/docs/current/userguide/build_environment.html

\# Specifies the JVM arguments used for the daemon process.
\# The setting is particularly useful for tweaking memory settings.
org.gradle.jvmargs=-Xmx1536m

\# When configured, Gradle will run in incubating parallel mode.
\# This option should only be used with decoupled projects. More details, visit
\# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects
\# org.gradle.parallel=true

\# AndroidX package structure to make it clearer which packages are bundled with the
\# Android operating system, and which are packaged with your app's APK
\# https://developer.android.com/topic/libraries/support-library/androidx-rn
android.useAndroidX=true
RELEASE_STORE_FILE=/build/apk_key.jks
RELEASE_STORE_PASSWORD=xxxxxx
RELEASE_KEY_ALIAS=alias
RELEASE_KEY_PASSWORD=xxxxxx

Replace both of the "xxxxxx" with an actual password. That password need to be at least 6 characters long.

- **Step 2**: In your terminal run `keytool -genkey -v -keystore apk_key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias alias;`.
It will ask for a keystore password, put the one you chose for the first step. It will follow by asking more information; those information don't need to be necesarilly true.
Enter 'y' to confirm the datas you entered.

- **Step 3**: run `docker build -t test -f android/Dockerfile . && docker run test:latest`.

- **Step 4**: Connect to http://localhost:8081/client.apk to download the mobile app.



### Services

- Server -> `http://localhost:8080/about.json`
- Web Client -> `http://localhost:8081/`
- Mobile Client APK -> YES

---

## 📜 API Example: `about.json`

WIP

---

## 🛠 Contributing

### Languages, frameworks and technologies

- Web App: React + SCSS
- Mobile App: React + Capacitor + SCSS
- Server: Python + fastapi
- Environment: Nix + Docker

### How to add a service

- Go to area/back/app/routes
- Add a folder and name it after the service you want to add
- Create a `__init__.py` file following other examples
- Create the .py file for the service and complete it following the other examples

### How to add an A-REA

WIP

---

## 📅 Project Timeline

- **21/09/2025**: Tech stack selection, PoC, task distribution.
- **06/10/2025**: Core architecture & base functionality.
- **02/11/2025**: Full feature set, UI, Docker deployment.

---

## 📖 Documentation

- **API**: http://localhost:8080/docs

keytool -genkey -v -keystore apk_key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias alias;

RELEASE_STORE_FILE=/build/apk_key.jks
RELEASE_STORE_PASSWORD=xxxx
RELEASE_KEY_ALIAS=alias
RELEASE_KEY_PASSWORD=xxxx