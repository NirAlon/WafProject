FROM python:3.13-slim
WORKDIR /app
COPY xss-service/requirements.txt .
RUN pip install -r requirements.txt
COPY common /app/common
COPY xss-service/app/ /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]