#1/bin/bash

helm \
  --kube-context minikube \
  upgrade \
  --install \
  --set service.type=NodePort \
  --set mysqlRootPassword=mysql \
  --set mysqlUser=mysql \
  --set mysqlPassword=my-mysql\
  --set mysqlDatabase=my-mysql \
  mysql \
  stable/mysql
