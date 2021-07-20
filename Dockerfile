# syntax=docker/dockerfile:1
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tz_shop

RUN apt-get update \
    && apt-get install -y postgresql-server-dev-11 gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY requirements.txt /tz_shop/
RUN pip install -r requirements.txt
COPY entrypoint.sh /tz_shop/
RUN chmod +x entrypoint.sh
COPY . /tz_shop/

EXPOSE 8000

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
