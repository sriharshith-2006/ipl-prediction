FROM python:3.11
WORKDIR /app
COPY api/requirements.txt .
RUN pip install -r requirements.txt
COPY api/ .
COPY models /models
EXPOSE 8000
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]