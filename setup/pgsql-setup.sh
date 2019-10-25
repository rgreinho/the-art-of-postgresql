#!/bin/bash

helm \
  --kube-context minikube \
  upgrade \
  --install \
  --set service.type=NodePort \
  --set postgresqlPassword=postgres \
  postgresql \
  stable/postgresql
