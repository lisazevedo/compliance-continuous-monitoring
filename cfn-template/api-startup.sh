#!/bin/bash
sudo apt update -y
sudo apt-get install -y \
    ca-certificates \
    curl \
    git \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose
sudo groupadd docker
sudo usermod -aG docker $USER
git clone https://github.com/lisazevedo/compliance-continuous-monitoring.git
cd compliance-continuous-monitoring
sudo docker-compose up -d 