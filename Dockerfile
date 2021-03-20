FROM python:3.8-slim

ADD ./ /opt

WORKDIR /opt

RUN pip install pipenv waitress && \
    pipenv install --system

ENTRYPOINT [ "waitress-serve", "--port=80", "app:app" ]