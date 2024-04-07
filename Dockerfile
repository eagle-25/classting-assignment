# 의존성 설치를 위한 베이스 이미지
FROM python:3.11.9-slim as builder

WORKDIR /app

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    PYTHONPATH="/app"

# Poetry 설치
RUN pip install "poetry==$POETRY_VERSION"

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock* /app/

# 프로젝트 의존성 설치
RUN poetry install --no-interaction --no-ansi

# 최종 스테이지
FROM python:3.11.9-slim as final

# 런타임을 위한 환경 변수 설정 (빌드 스테이지에서 설정된 환경 변수는 최종 이미지로 이어지지 않음)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    PYTHONPATH="/app"

WORKDIR /app

# 개선 필요
COPY --from=builder / /
COPY . /app