FROM python:3.12.11-alpine3.22

WORKDIR /app

ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8080
# ENV FLASK_ENV development
# ENV FLASK_DEBUG 1

COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["flask", "run"]