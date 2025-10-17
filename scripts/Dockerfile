FROM python:3.12.11-alpine3.22

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# run database migrations
# RUN alembic upgrade head

EXPOSE 8080
