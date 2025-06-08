FROM python:3.11-slim

RUN pip install python-owasp-zap-v2.4

WORKDIR /app

COPY zap_scan.py .

ENTRYPOINT ["python3", "zap_scan.py"]
