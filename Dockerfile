FROM python:3.12-slim

# Java ve apktool için bağımlılıklar
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless \
    wget \
    && rm -rf /var/lib/apt/lists/*

# apktool kur (sabit sürüm — resmi GitHub releases sayfasından mevcut son sürüm: v3.0.2)
ARG APKTOOL_VERSION=3.0.2
RUN wget -q \
    https://github.com/iBotPeaches/Apktool/releases/download/v${APKTOOL_VERSION}/apktool_${APKTOOL_VERSION}.jar \
    -O /usr/local/lib/apktool.jar && \
    printf '#!/bin/sh\nexec java -jar /usr/local/lib/apktool.jar "$@"\n' \
    > /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Klasörlerin var olduğundan emin ol
RUN mkdir -p apks reports

ENTRYPOINT ["python", "src/main.py"]
CMD ["--help"]
