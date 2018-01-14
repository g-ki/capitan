FROM python:3.5

# Create app directory
ENV INSTALL_PATH /capitan
RUN mkdir -p ${INSTALL_PATH}

WORKDIR ${INSTALL_PATH}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
