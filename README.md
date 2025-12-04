# Real-Time Microphone Transcription

A Dockerized, real-time speech-to-text application built with **Django**, **WebSockets (Django Channels)**, and the **Vosk** offline speech recognition engine.

This project demonstrates a CPU-only, privacy-first approach to transcription where audio is streamed directly from the browser to the backend for immediate inference.

## 🚀 Key Features
* **Real-Time Streaming:** Bi-directional audio streaming using WebSockets.
* **CPU-Only Inference:** Uses the lightweight Vosk model (Kaldi-based), requiring no GPU.
* **Live Feedback:** Displays partial (gray) and final (black) transcripts in real-time.
* **Data Persistence:** Saves session metadata, duration, final text, and word count to SQLite.
* **Dockerized:** Fully reproducible environment using Docker Compose.

## 🛠️ Technology Stack
* **Backend:** Python 3.13, Django 6
* **Async:** Django Channels, Daphne (ASGI)
* **AI Model:** Vosk (Small English Model 0.15)
* **Frontend:** HTML5, JavaScript (AudioContext API)
* **Infrastructure:** Docker, Docker Compose

---

## 📦 Setup & Installation Instructions

**Prerequisites:** You must have [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

### 1. Get the Code
Clone this repository or unzip the project folder.


Download the AI Model (Critical Step)

The AI model is not included in the source code to minimize file size. You must download it manually.

    Download the Vosk Small English Model (approx. 40MB):

    https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

    Create a folder named model in the root of the project directory.

    Unzip the downloaded file into the model folder.

Before starting the server for the first time, you must generate and apply the database migrations to create the SQLite database file.

Run these commands in your terminal:

**Build the container:**

`docker-compose build`

**Generate Migration Files:**

`docker-compose run web python manage.py makemigrations`


Now that the model, database and SERVER are ready:

http://localhost:8000

http://localhost:8000/api/sessions/
