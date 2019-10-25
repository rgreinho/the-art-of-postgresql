#!/bin/bash

export POSTGRES_PASSWORD=$(kubectl get secret --namespace default postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode)
# export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
export NODE_IP=$(minikube ip)
export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services postgresql)
echo "export PGHOST=${NODE_IP}"
echo "export PGPORT=${NODE_PORT}"
echo "export PGUSER=postgres"
echo "export PGPASSWORD=${POSTGRES_PASSWORD}"
echo "# To connect, run:"
echo "#   pgcli postgres://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/postgres"
