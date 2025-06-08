FROM zaproxy/zap-stable

USER root

# Installer Python 3 et pip (si pas déjà dedans)
RUN apt-get update && apt-get install -y python3 python3-pip

# Installer la lib Python pour zap
RUN pip3 install python-owasp-zap-v2.4

COPY zapscan.py /app/zapscan.py

WORKDIR /app

ENTRYPOINT ["python3", "zapscan.py"]
