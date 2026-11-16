FROM python:3.13-slim-bookworm AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_SYSTEM_PYTHON=true

RUN pip install --no-cache-dir uv==0.12.4

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev
COPY src /app/src
RUN uv sync --frozen --no-dev

FROM python:3.13-slim-bookworm

RUN groupadd -r -g 1000 appuser && \
    useradd -r -u 1000 -g appuser -d /app -s /usr/sbin/nologin appuser

COPY --from=builder --chown=appuser:appuser /app /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app/src

USER appuser

EXPOSE 8000

CMD ["uvicorn", "order_service.app.main:create_app", "--factory", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]
