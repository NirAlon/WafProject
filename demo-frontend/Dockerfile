FROM python:3.13-slim
WORKDIR /app
ENV FLASK_ENV development
COPY demo-frontend/requirements.txt .
RUN pip install -r requirements.txt
COPY demo-frontend/app/ /app/
CMD ["python", "app.py"]