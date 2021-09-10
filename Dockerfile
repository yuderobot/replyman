FROM python:3.8.11-alpine3.13
ADD ./ /app

# Install dependencies
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev git

# Set working directory
WORKDIR /app/src

## Python packages
RUN pip install -r requirements.txt

# Run the bot
ENTRYPOINT ["python", "main.py"]
