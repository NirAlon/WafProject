FROM python:3.13-slim
WORKDIR /app
COPY orchestrator/requirements.txt .
RUN pip install -r requirements.txt
COPY orchestrator/app/ /app/
COPY common /app/common
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]