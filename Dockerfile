FROM python:3.8-slim

LABEL org.opencontainers.image.source https://github.com/Accendit/azdevops_discord

ADD ./ /opt

WORKDIR /opt

RUN pip install pipenv waitress && \
    pipenv install --system

ENTRYPOINT [ "waitress-serve", "--port=80", "app:app" ]