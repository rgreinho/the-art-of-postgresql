#!/bin/bash

MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)
# MYSQL_HOST=$(kubectl get nodes --namespace default -o jsonpath='{.items[0].status.addresses[0].address}')
PORT=$(kubectl get svc --namespace default mysql -o jsonpath='{.spec.ports[0].nodePort}')
echo "export MYSQL_HOST=$(minikube ip)"
echo "export MYSQL_PORT=${PORT}"
echo "export MYSQL_PWD=${MYSQL_ROOT_PASSWORD}"

echo "# To connect, run:"
# echo "# mysql -h ${MYSQL_HOST} -P${MYSQL_PORT} -u root -p${MYSQL_PWD}"
echo '# mycli mysql://root:${MYSQL_PWD}@${MYSQL_HOST}:${MYSQL_PORT}/mysql'
