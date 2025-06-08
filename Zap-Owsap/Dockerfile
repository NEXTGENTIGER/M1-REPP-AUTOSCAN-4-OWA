# Base image avec Python 3.11
FROM python:3.11-slim

# Installer dépendances système (curl pour tester la connectivité)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Installer la lib Python ZAP
RUN pip install python-owasp-zap-v2.4

# Copier le script dans le container
COPY zapscan.py /app/zapscan.py

WORKDIR /app

CMD ["python", "zapscan.py"]
