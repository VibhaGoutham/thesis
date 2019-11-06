#!/bin/bash

curl -k -X POST \
  https://admin:password@10.20.5.34/rest/playbook_run \
  -H 'Content-Type: application/json' \
  -H 'G-TOKEN: 95e3bcff-bfca-454d-b59e-768da6280c38' \
  -H 'Postman-Token: 73ee5c01-48cf-431e-b065-d437dd3f7a81' \
  -H 'cache-control: no-cache' \
  -d '{
  "container_id": 357,
  "playbook_id": "local/sarnet case 1",
  "scope": "new",
  "run": true
}'
