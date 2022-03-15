FROM python:3.9.10-bullseye AS builder

# Copy requirements.txt from host
ADD ./src/requirements.txt /

## Install Python packages
RUN pip install $(grep -ivE "numpy" requirements.txt)

FROM python:3.9.10-bullseye AS runner

# Copy dependencies from builder / Install dependencies
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
RUN apt -y update; apt -y install git python3-numpy

# Copy app from host
ADD ./ /app
WORKDIR /app/src

# Run the bot
ENTRYPOINT ["python", "main.py"]
