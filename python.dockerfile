FROM python:3-slim

RUN useradd -m -u 1000 appuser

COPY . /app
WORKDIR /app

RUN chown -R appuser:appuser /app

USER appuser

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
