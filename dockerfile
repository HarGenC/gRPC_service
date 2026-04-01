FROM python:3.13-slim

RUN addgroup --system --gid 1001 appgroup
RUN adduser --system --uid 1001 --ingroup appgroup appuser

RUN pip install --no-cache-dir uv

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_CACHE=1

WORKDIR /app
RUN chown -R appuser:appgroup /app
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

USER appuser

CMD ["python", "server.py"]