FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY 1_раздел/script.py /app/script.py

CMD ["python3", "script.py"]
