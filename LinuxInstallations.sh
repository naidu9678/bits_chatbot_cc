#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display messages
echo_msg() {
    echo -e "\n=== $1 ===\n"
}

# Update and upgrade the system
echo_msg "Updating and upgrading system packages"
sudo apt-get update -y
sudo apt-get upgrade -y

# Install prerequisite packages
echo_msg "Installing prerequisite packages"
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release net-tools iputils-ping telnet


# -------------------------------
# Install Docker
# -------------------------------
echo_msg "Installing AWS CLI"

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# -------------------------------
# Install Docker
# -------------------------------
echo_msg "Installing Docker"

# Remove any old Docker versions
sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

# Add Docker’s official GPG key
echo_msg "Adding Docker's GPG key"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the Docker repository
echo_msg "Setting up Docker repository"
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index
sudo apt-get update -y

# Install Docker Engine
echo_msg "Installing Docker Engine"
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Enable and start Docker service
echo_msg "Enabling and starting Docker service"
sudo systemctl enable docker
sudo systemctl start docker

# Optional: Add current user to the Docker group (requires logout/login)
# sudo usermod -aG docker $USER
# echo "You might need to log out and log back in to apply Docker group changes."

# -------------------------------
# Install Kubernetes Tools (kubeadm, kubelet, kubectl)
# -------------------------------
echo_msg "Installing Kubernetes tools (kubeadm, kubelet, kubectl)"

# Add Kubernetes’ official GPG key
echo_msg "Adding Kubernetes' GPG key"
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/kubernetes-archive-keyring.gpg

# Add Kubernetes apt repository
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Update package index
sudo apt-get update -y

# Install kubelet, kubeadm, and kubectl
sudo apt-get install -y kubelet kubeadm kubectl

# Hold Kubernetes packages at current version to prevent accidental upgrades
sudo apt-mark hold kubelet kubeadm kubectl

# -------------------------------
# Install Helm
# -------------------------------
echo_msg "Installing Helm"

# Download and install Helm
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify Helm installation
helm version

# -------------------------------
# Install Git
# -------------------------------
echo_msg "Installing Git"
sudo apt-get install -y git

# -------------------------------
# Install Python3
# -------------------------------
echo_msg "Installing Python3"
sudo apt-get install -y python3 python3-pip

# -------------------------------
# Cleanup
# -------------------------------
echo_msg "Cleaning up unnecessary packages"
sudo apt-get autoremove -y

echo_msg "All tasks completed successfully!"