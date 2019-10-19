#!/bin/bash
set -euo pipefail

# Define variables.
C_GREEN='\033[32m'
C_RED='\033[31m'
C_RESET_ALL='\033[0m'

# Install packages if needed.
minikube version || brew cask install minikube
helm version -c || brew install kubernetes-helm

# Install addons.
mkdir -p ~/.minikube/addons

# (Re)Start the service.
# shellcheck disable=SC1083
MINIKUBE_STATUS=$(minikube status --format  {{.MinikubeStatus}} || true)
if [ "${MINIKUBE_STATUS}" == "Paused" ] || [ "${MINIKUBE_STATUS}" == "Stopped" ] || [ -z "${MINIKUBE_STATUS}" ]; then
  echo -e "${C_GREEN}Starting Minikube...${C_RESET_ALL}"
  minikube start --vm-driver virtualbox --memory 4096 --cpus 4 --kubernetes-version=1.15.4
elif [ "${MINIKUBE_STATUS}" == "Running" ]; then
  echo -e "${C_GREEN}Minikube is already running.${C_RESET_ALL}"
else
  echo -e "${C_RED}Minikube is in an unknown state.${C_RESET_ALL}"
  echo -e "${C_RED}Please run 'minikube status' and fix the problem manually.${C_RESET_ALL}"
  exit 1
fi

# Set up Minikube context.
echo -e "${C_GREEN}Configuring minikube context...${C_RESET_ALL}"
kubectl config use-context minikube

# Set up Helm.
while ! helm init --wait 2>/dev/null; do
  echo -e "${C_RED}Helm init has not completed yes...${C_RESET_ALL}"
  sleep 1
done

# This is a hack to ensure tiller is ready.
echo -ne "${C_GREEN}Waiting for Tiller to start..."
while ! helm ls 2>/dev/null; do
  echo -ne "."
  sleep 1
done
echo -e "${C_RESET_ALL}"

# Add/Update Helm chart repositories.
# helm repo add ryr https://charts.requestyoracks.org
helm repo update

# Display a message to tell to update the environment variables.
minikube docker-env

# Enable addons
minikube addons enable heapster
minikube addons enable ingress

# Wait for the dashboard to be ready.
echo -e -n "${C_GREEN}Waiting for the dashboard to be ready...${C_RESET_ALL}"
until minikube service -n kube-system kubernetes-dashboard >/dev/null 2>&1; do
  echo -e -n "${C_GREEN}.${C_RESET_ALL}"
  sleep 1
done
echo
