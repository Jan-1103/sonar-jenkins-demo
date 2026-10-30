#!/bin/bash
# Run on a fresh Ubuntu 22.04/24.04 EC2 (t3.medium or bigger):  bash ec2-setup/setup-ec2.sh
set -e
sudo apt-get update
sudo apt-get install -y fontconfig openjdk-17-jre git unzip curl python3 python3-venv python3-pip docker.io

# Jenkins
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt-get update
sudo apt-get install -y jenkins
sudo systemctl enable --now jenkins

# SonarQube needs this kernel setting
sudo sysctl -w vm.max_map_count=262144
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf

# SonarQube in Docker
sudo systemctl enable --now docker
sudo docker run -d --name sonarqube --restart unless-stopped -p 9000:9000 sonarqube:community

echo "Jenkins initial password:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
echo "Jenkins: http://<EC2-PUBLIC-IP>:8080   SonarQube: http://<EC2-PUBLIC-IP>:9000 (admin/admin)"
