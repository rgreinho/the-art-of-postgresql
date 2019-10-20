#!/bin/bash

helm install --name postgresql \
  --set service.type=NodePort \
  --set postgresqlPassword=postgres \
  stable/postgresql
