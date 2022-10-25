FROM python:3.10.1-slim-bullseye

LABEL description="Chromo housing back-end application."
LABEL maintainer="Vladimir Carpa <oswalth2@gmail.com>"

# Setup application home
ENV APP_HOME="/app"

# Setup application (non-root) user
ENV APP_USER="app"
RUN groupadd -r ${APP_USER} \
    && useradd -r -g ${APP_USER} -d ${APP_HOME} -s /sbin/nologin -c "bisque application user" -m ${APP_USER}


# Create poetry home directory
ENV POETRY_HOME="/opt/poetry"
RUN mkdir ${POETRY_HOME} && chown ${APP_USER}:${APP_USER} ${POETRY_HOME}

# Change to the project directory & project user
WORKDIR ${APP_HOME}
USER ${APP_USER}:${APP_USER}

ENV PATH="${POETRY_HOME}/bin:${PATH}"
ENV PIP_DISABLE_PIP_VERSION_CHECK="on"
ENV PYTHONUNBUFFERED="1"

ENV POETRY_VERSION="1.2.2"

RUN python3 -m venv ${POETRY_HOME} \
    && ${POETRY_HOME}/bin/pip install --upgrade pip \
    && ${POETRY_HOME}/bin/pip install --no-cache-dir poetry==${POETRY_VERSION}


# Install project dependencies
COPY ./pyproject.toml ./
COPY ./poetry.toml ./
COPY ./poetry.lock ./

# Copy project source & install it
COPY ./src ./src

RUN poetry install \
    && rm -rf ~/.cache/pypoetry/

ARG DEBUG=${DEBUG:-"false"}
# Setup project env vars
ENV DEBUG="${DEBUG}"
ENV DJANGO_HOST="0.0.0.0"
ENV DJANGO_PORT="9050"

# Expose backend port
EXPOSE ${DJANGO_PORT}

# Setup entrypoint and make it executable
COPY ./entrypoint.sh .
USER root
RUN chmod +x ./entrypoint.sh
USER ${APP_USER}:${APP_USER}

CMD ["poetry", "run", "gunicorn", "-c", "/app/src/gunicorn_conf.py"]
