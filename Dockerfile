FROM python:3.11.9-slim

WORKDIR /app

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_VERSION=1.6.1 \
    PYTHONPATH="/app"

# Poetry 설치
RUN pip install "poetry==$POETRY_VERSION"

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock* /app/

# 프로젝트 의존성 설치
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# 애플리케이션 파일 복사
COPY . /app