#!/bin/bash

set -e

echo -n "Quay.io Username: " >&2
read USERNAME
echo -n "Quay.io Password: " >&2
read -s PASSWORD
echo

token=$(curl -H "Content-Type: application/json" -XPOST https://quay.io/cnr/api/v1/users/login -d '
{
    "user": {
        "username": "'"${USERNAME}"'",
        "password": "'"${PASSWORD}"'"
    }
}' | jq '.token')

echo $token | xargs echo > .token
