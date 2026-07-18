<div align="center">

# 🏡 Home Price Predictor — Web & API

**A full-stack machine learning application that predicts real estate prices across Bangalore, India**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Linear%20Regression-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)

</div>

---

## 📖 Overview

This repository contains the core intelligence of the Home Price prediction platform — a trained ML model, a Flask REST API that serves live predictions, and a responsive web frontend, all designed to run behind an Nginx reverse proxy for production-grade performance.

---

## ✨ Features

| | |
|---|---|
| 🧠 **Machine Learning Engine** | Custom-trained Scikit-Learn Linear Regression model for price estimation |
| 🔌 **RESTful API** | Structured JSON endpoints consumable by web, mobile, or desktop clients |
| 🖥️ **Web Interface** | Fully responsive browser UI built with HTML, CSS, and jQuery |
| 🚀 **Production Ready** | Nginx-backed routing and static file delivery |

---

## 🛠️ Tech Stack

**Machine Learning** — Scikit-Learn · NumPy · Pandas
**Backend** — Python · Flask
**Frontend** — HTML5 · CSS3 · Vanilla JavaScript (jQuery)
**Web Server** — Nginx

---

## 📂 Directory Structure

```
Home-Prices-API/
│
├── client/               # HTML/CSS/JS frontend UI
├── model/                # Jupyter notebooks & ML artifacts (.pickle, columns.json)
├── nginx_files/          # Nginx reverse proxy configurations
├── server/               # Flask REST API (server.py, util.py)
└── README.md             # You are here
```

---

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.x
- Nginx installed locally or on your host server

### 1. Start the Flask Backend

Clone the repository and move into the `server` folder:

```bash
git clone https://github.com/Shashank17singh/Home-Prices-API.git
cd Home-Prices-API/server
```

Install the required libraries:

```bash
pip install flask numpy scikit-learn
```

Run the server:

```bash
python server.py
```

The server loads the ML artifacts and listens on port `5000`.

### 2. Configure Nginx

To serve the frontend and proxy API requests, update your local `nginx.conf` server block (a reference config is also in `nginx_files/`):

```nginx
server {
    listen       80;
    server_name  localhost;

    # Serve Frontend UI
    location / {
        root   "C:/Path/To/Your/Project/Bangalore-Home-Prices-API/client"; # Update this path!
        index  app.html index.html index.htm;
    }

    # Proxy API requests to Flask
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://127.0.0.1:5000;
    }
}
```

Reload Nginx (`nginx -s reload`) and open `http://localhost` in your browser.

---

## 📡 API Documentation

### `GET /get_location_names`

Returns all supported Bangalore neighborhoods.

**Response**
```json
{
  "locations": ["1st Phase JP Nagar", "Electronic City", "Whitefield", "..."]
}
```

### `POST /predict_home_price`

Calculates the estimated price in Lakh Rupees.

**Form Data Parameters**

| Parameter | Type | Description |
|---|---|---|
| `total_sqft` | float | Total square footage |
| `bhk` | int | Number of bedrooms |
| `bath` | int | Number of bathrooms |
| `location` | string | Neighborhood name |

**Response**
```json
{
  "estimated_price": 86.81
}
```

---
