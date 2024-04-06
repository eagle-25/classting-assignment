FROM python:3.11.9-slim

WORKDIR /app
COPY . /app

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    PYTHONPATH="/app"

# Poetry 설치
RUN pip install -r ./requirements.txt

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock* /app/

# 프로젝트 의존성 설치
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

