FROM python:3.9.10-alpine3.15 AS builder

# Install dependencies
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev git

# Copy requirements.txt from host
ADD ./src/requirements.txt /

## Install Python packages
RUN pip install $(grep -ivE "numpy" requirements.txt)

FROM python:3.9.10-alpine3.15 AS runner

# Copy dependencies from builder / Install dependency
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
RUN apk add py3-numpy 

# Copy app from host
ADD ./ /app
WORKDIR /app/src

# Run the bot
ENTRYPOINT ["python", "main.py"]
