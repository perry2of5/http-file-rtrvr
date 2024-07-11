# Here we build layers in the builder that depend on poetry and then copy the virtual environment
# to the runtime. This way we get a 159 MB image instead of a 270 MB image.

############ builder (contains poetry) ############
FROM python:3.12.7-bullseye AS builder
    

RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1


# add user for python-slim
RUN useradd -ms /bin/bash svcuser
RUN chown svcuser:svcuser /home/svcuser
USER svcuser
WORKDIR /home/svcuser


COPY --chown=svcuser:svcuser pyproject.toml poetry.lock ./
RUN touch README.md
RUN poetry lock --no-update
# we could cache the poetry cache instead https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
RUN poetry install --without test --no-root --no-cache


############ runtime without poetry so it is smaller ############
FROM python:3.12.7-slim-bullseye AS runtime


# install azure cli -- only needed for running in local docker.
# RUN apt-get update
# RUN apt-get install curl -y
# RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash


# add user for python-slim
RUN useradd -ms /bin/bash svcuser
RUN chown svcuser:svcuser /home/svcuser
USER svcuser

# ensure expected temp dir will exist and is only readable by svcuser
WORKDIR /home/svcuser/tmp/http_rtrvr_temp
USER root
RUN chown svcuser:svcuser /home/svcuser/tmp/http_rtrvr_temp
RUN chmod 700 /home/svcuser/tmp/http_rtrvr_temp
USER svcuser
# change to home directory
WORKDIR /home/svcuser


ENV VIRTUAL_ENV=/home/svcuser/.venv \
    PATH="/home/svcuser/.venv/bin:$PATH" \
    PYTHONPATH=.

# copy the dependencies from the builder
COPY --chown=svcuser:svcuser --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# now copy the code from our project
COPY --chown=svcuser:svcuser http_file_rtrvr http_file_rtrvr/

# CMD [ "python", "-c", "import os; print(os.getcwd()); import time; time.sleep(600)" ] # sleep 10 minutes for debugging
# CMD [ "sleep", "600"]

# run the environment-variable-based http file retriever
# CMD [ "python3", "http_file_rtrvr/env_var_http_file_rtrvr.py" ]
CMD [ "python3", "http_file_rtrvr/azure_svc_bus_http_file_rtrvr.py" ]