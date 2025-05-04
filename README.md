# Web Application Firewall (WAF)

A Django‐based Web Application Firewall that uses deep learning (CNN on TensorFlow) to detect and block XSS, SQL Injection, and CSRF attacks at the HTTP/S layer.

---

## Project Overview

This project is built around a demo website that lets you trigger optional cyber-attack payloads via two REST API endpoints (`/sql_api` and `/xss_api`). Under the hood, two Docker containers run TensorFlow Serving—each hosting a trained CNN model (one for SQL injection, one for XSS). When a request arrives, the Django server forwards the raw input to the appropriate TF-Serving container, receives a real-time prediction score, and then decides whether to block or allow the request before sending its response back to the client.

---

## Table of Contents  
1. [Features](#Features)  
2. [Prerequisites](#Prerequisites)  
3. [Installation & Setup](#installation--setup)  
4. [Deploying the Models with Docker](#Deploying-the-models-with-docker)  
5. [Demo Site](#demo-site)  
6. [Contributing](#contributing)  
7. [Demo & API Testing](#demo--api-testing)  

---

## Features
- Deep Learning Detection using Convolutional Neural Networks  
- REST API endpoints: `/sql_api` and `/xss_api`  
- Web-based log viewer for incoming requests and WAF decisions  
- Tested on AWS EC2 (HTTPS optional)  

---


## Prerequisites
- Python 3.8 or higher  
- Docker (for model serving)  
- Postman or cURL for API testing  

---

## Installation & Setup
1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/waf-project.git
   cd waf-project
   ```
2. Create and activate a virtual environment  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. install Python dependencies
   ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
4.  Apply migrations and (optionally) create a superuser
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```
5. Running the Django Server
    ```bash
    python manage.py runserver
    ```
*Open your browser at http://127.0.0.1:8000/demo_site*
***
## Deploying the models with docker

Deploy SQL container

1. Download the pre-trained models from Google Drive
https://drive.google.com/file/d/1yvDGWF2v7DdcjaNwYqnGr7cprvjwjd89/view?usp=sharing

2. Start the SQL model server
```bash
docker run -p 8500:8501 --name tfserving_sql --mount type=bind,source=/path/to/sqlmodel/1,target=/bitnami/model-data/1 -e TENSORFLOW_SERVING_MODEL_NAME=sqlmodel bitnami/tensorflow-serving:latest
```
3. Start the XSS model server
```bash
docker run -p 8501:8501 \
  --name tfserving_xss \
  --mount type=bind,source=/path/to/xssmodel/1,target=/bitnami/model-data/1 \       
  -e TENSORFLOW_SERVING_MODEL_NAME=xssmodel \
  bitnami/tensorflow-serving:latest
```
***
## Demo Site
Reflected XSS, SQL Injection, and Stored XSS scenarios are available at:
http://127.0.0.1:8000/demo_site
***
## Contributing
1. Fork the repository

2. Create a feature branch: git checkout -b feature/my-change

3. Commit your changes: git commit -m "Add my feature"

4. Push to your fork: git push origin feature/my-change

5. Open a Pull Request

## Demo & API Testing
![](sql_demo_api.gif)

{
"text":"enter xss code OR any other text"
}
![](xss_demo_api.gif)

![](xss_attack.gif)
![](sql_injection.gif)
![](xss_attack_stored.gif)



