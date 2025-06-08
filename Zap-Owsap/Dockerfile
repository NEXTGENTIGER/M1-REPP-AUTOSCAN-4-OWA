FROM zaproxy/zap-stable

USER root

# Installer Python 3 et pip si nécessaire
RUN apt-get update && apt-get install -y python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Installer la lib python pour zap
RUN pip3 install --no-cache-dir python-owasp-zap-v2.4

COPY zapscan.py /app/zapscan.py
WORKDIR /app

ENTRYPOINT ["python3", "zapscan.py"]
