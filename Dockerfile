FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt app.zip ./
RUN pip install --no-cache-dir -r requirements.txt \
 && python -m zipfile -e app.zip . \
 && rm app.zip
ENV PORT=8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 2 --proxy-headers --forwarded-allow-ips='*'"]
