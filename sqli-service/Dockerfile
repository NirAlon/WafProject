FROM python:3.13-slim
WORKDIR /app
COPY sqli-service/requirements.txt .
RUN pip install -r requirements.txt
COPY common /app/common
COPY sqli-service/app /app/
COPY sqli-service/vectorizer_cnn.pkl /app/vectorizer_cnn.pkl
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]