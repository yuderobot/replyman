FROM python:3.8.11-alpine3.13
ADD ./src /src

# Set working directory
WORKDIR /src

## Python packages
WORKDIR /src
RUN pip install -r requirements.txt

# Run crond
ENTRYPOINT ["python", "main.py"]