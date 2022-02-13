# FROM python:3.7
# FROM python:3.8-slim-buster

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:slim


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get upgrade -y && apt-get install -y
RUN apt-get update && apt-get -y install sudo


# RUN apt-get update && apt-get upgrade -y \
#     && apt-get install -y \
#         apt-transport-https \
#         libpq-dev \
#         libmariadb-dev \
#         default-libmysqlclient-dev \
#         build-essential \
#         git \
#         sudo \
#         cmake zlib1g-dev libjpeg-dev xvfb xorg-dev libboost-all-dev libsdl2-dev swig ca-certificates \
#         unzip zip nano\
#         poppler-utils \
#         curl\
#         libtesseract-dev \
#         python-dev libxml2-dev libxslt1-dev antiword\
#         unoconv\
#         ffmpeg libsm6 libxext6\
#     && rm -rf /var/lib/apt/lists/*


# Get protoc 3.0.0, rather than the old version already in the container

# RUN curl -k -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
#     unzip protoc-3.0.0-linux-x86_64.zip -d proto3 && \
#     mv proto3/bin/* /usr/local/bin && \
#     mv proto3/include/* /usr/local/include && \
#     rm -rf proto3 protoc-3.0.0-linux-x86_64.zip


# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH=$PYTHONPATH:/models/research/slim
ENV PYTHONPATH=$PYTHONPATH:/models/research


COPY ./requirements.txt /root/requirements.txt
RUN pip install --use-deprecated=legacy-resolver -r /root/requirements.txt
# RUN python -m pip install -r requirements.txt


WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8009", "main.wsgi"]

CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8009"]
