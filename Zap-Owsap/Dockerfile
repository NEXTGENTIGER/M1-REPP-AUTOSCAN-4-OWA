# Base image Python légère
FROM python:3.11-slim

# Met à jour les paquets et installe curl (utile pour healthcheck éventuel)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Crée un dossier de travail
WORKDIR /app

# Copie les fichiers nécessaires dans le container
COPY zapscan.py /app/

# Installe la librairie zapv2 pour interagir avec ZAP API
RUN pip install --no-cache-dir python-owasp-zap-v2.4

# Volume pour résultats (facultatif ici, tu peux monter depuis docker-compose)
VOLUME ["/app/results"]

# Commande par défaut, attends que TARGET_URL soit passé via variable d'env
ENTRYPOINT ["python3", "zapscan.py"]
