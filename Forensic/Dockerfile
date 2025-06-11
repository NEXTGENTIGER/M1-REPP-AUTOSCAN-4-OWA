FROM python:3.11-slim

# Installer les paquets Debian disponibles
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
    file \
    python3-dev \
    libfuse2 \
    && apt-get clean

# Installer UPX manuellement
RUN wget https://github.com/upx/upx/releases/download/v4.0.1/upx-4.0.1-amd64_linux.tar.xz && \
    tar -xf upx-4.0.1-amd64_linux.tar.xz && \
    mv upx-4.0.1-amd64_linux/upx /usr/local/bin/ && \
    rm -rf upx-4.0.1-amd64_linux*

# Installer radare2 manuellement
RUN git clone https://github.com/radareorg/radare2.git /radare2 && \
    cd /radare2 && \
    sys/install.sh && \
    cd / && \
    rm -rf /radare2

# Mettre à jour la base de données ClamAV
RUN freshclam

# Installer les packages Python
RUN pip install peframe plaso

# Installer volatility3
RUN git clone https://github.com/volatilityfoundation/volatility3 /opt/volatility3 && \
    pip install -r /opt/volatility3/requirements.txt && \
    ln -s /opt/volatility3/vol.py /usr/local/bin/vol.py

CMD ["/bin/bash"]
