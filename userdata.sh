#!/bin/bash
set -eux

# Packages
dnf -y update
dnf -y install git docker

# Docker engine & Compose v2
systemctl enable --now docker
usermod -aG docker ec2-user
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
     -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# OPTIONAL: pull your repo & start the stack
git clone https://github.com/DrCBeatz/springbrookfarmhouse.git /opt/app
cd /opt/app && docker compose up -d
