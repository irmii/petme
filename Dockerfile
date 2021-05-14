FROM python:3.8-slim
LABEL description="App контейнер уровня нуля."

ARG BUILD_PACKAGES="gcc g++ software-properties-common apt-transport-https apt-utils gnupg1 libcurl4-openssl-dev libssl-dev git-core"
ARG BUILD_DEPS="netcat ca-certificates"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -ex && \
    apt-get update && \
    apt-get install -y --no-install-recommends $BUILD_PACKAGES && \
    rm -rf /var/lib/apt/lists/*

RUN set -ex && \
    apt-get update && \
    apt-get install -y --no-install-recommends $BUILD_DEPS && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY Pipfile /code/
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN set -ex && \
    pip3 install pipenv && \
    pipenv lock && \
    pipenv install $( [ "$DJANGO_ENV" = "production" ] || echo "--dev" ) --deploy --system --ignore-pipfile && \
    chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]