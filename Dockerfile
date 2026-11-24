# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.txt ./
RUN python -m venv /opt/venv && /opt/venv/bin/pip install -r requirements.txt

FROM python:3.12-slim
LABEL org.opencontainers.image.title="demo-reviews-api" \
      org.opencontainers.image.description="Customer reviews service - Demo Commerce Platform" \
      org.opencontainers.image.source="https://github.com/renanlJ/demo-reviews-api" \
      org.opencontainers.image.licenses="MIT"
ENV PATH=/opt/venv/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY --from=build /opt/venv /opt/venv
WORKDIR /app
COPY app ./app
RUN useradd --system --uid 10001 --create-home appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
