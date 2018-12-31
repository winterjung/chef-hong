FROM python:3.7-alpine as BUILDER

LABEL maintainer="wintermy201@gmail.com"

RUN apk update \
    && apk add gcc musl-dev python3-dev libxslt-dev

WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM python:3.7-alpine

COPY --from=BUILDER /install /usr/local
RUN apk add libxslt-dev

WORKDIR /usr/src/chef

COPY app app
COPY migrations migrations
COPY manage.py manage.py
COPY config.py config.py

EXPOSE 8000
ENV FLASK_CONFIG production
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["gunicorn"]
CMD ["manage:app", "-k", "gevent", "-b", "0.0.0.0:8000", "--timeout", "43200"]
