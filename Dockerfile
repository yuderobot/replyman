FROM python:3.9.10-alpine3.15 AS builder

# Install dependencies
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev git

# Copy requirements.txt from host
ADD ./src/requirements.txt /

## Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9.10-alpine3.15 AS runner

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app from host
ADD ./ /app
WORKDIR /app/src

# Run the bot
ENTRYPOINT ["python", "main.py"]
