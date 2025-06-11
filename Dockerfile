FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git curl wget unzip nano \
    build-essential \
    libffi-dev libssl-dev \
    p7zip-full \
    exiftool \
    yara \
    clamav \
    binwalk \
    foremost \
    hashdeep \
    ssdeep \
    binutils \
    upx \
    radare2 \
    file \
    strings \
    python3-dev \
    libfuse2 \
    && apt-get clean

RUN freshclam

RUN pip install peframe plaso

RUN git clone https://github.com/volatilityfoundation/volatility3 /opt/volatility3 && \
    pip install -r /opt/volatility3/requirements.txt && \
    ln -s /opt/volatility3/vol.py /usr/local/bin/vol.py

CMD ["/bin/bash"]
