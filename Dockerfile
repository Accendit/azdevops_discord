FROM python:3.8-slim

LABEL org.opencontainers.image.source https://github.com/Accendit/azdevops_discord

ADD azdevops_discord/* /opt/azdevops_discord/azdevops_discord/

ADD Pipfile* /opt/azdevops_discord

WORKDIR /opt/azdevops_discord

RUN pip install pipenv waitress && \
    pipenv install --system

ENTRYPOINT [ "waitress-serve", "--port=80", "azdevops_discord:app" ]