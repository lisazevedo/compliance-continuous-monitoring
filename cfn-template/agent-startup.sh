#!/bin/bash
sudo apt update -y
sudo apt install git python3-pip -y
wget https://raw.githubusercontent.com/lisazevedo/compliance-continuous-monitoring/main/agent/requirements.txt
pip3 install -r requirements.txt
wget https://raw.githubusercontent.com/lisazevedo/compliance-continuous-monitoring/main/agent/agent.py