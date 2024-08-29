FROM python:3-slim

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
