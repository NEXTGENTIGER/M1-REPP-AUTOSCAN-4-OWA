FROM owasp/zap2docker-stable

USER root

# Installer python3 et pip (si non déjà dans l’image)
RUN apt-get update && apt-get install -y python3 python3-pip

# Installer dépendances python
RUN pip3 install python-owasp-zap-v2.4

# Copier le script dans le conteneur
COPY zapscan.py /app/zapscan.py

WORKDIR /app

# Par défaut, la commande attendra les arguments (target)
ENTRYPOINT ["python3", "zapscan.py"]
