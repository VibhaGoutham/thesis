#!/bin/bash

curl -X POST \
  http://10.20.4.80:5000/v3/auth/tokens \
  -H 'Accept-Encoding: UTF-8' \
  -H 'Authorization: Basic dmliaGE6aGVsbG8xMjM=' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: ef1f2c14-104b-4626-b374-54a028ed187e' \
  -H 'cache-control: no-cache' \
  -d '{
    "auth": {
        "identity": {
            "methods": [
                "token"
            ],
            "token": {
                "id": 
"gAAAAABciRm8eNIs3ou17CFygUuEWsFg4_VRvnL16LAwB-oyf5k1j9IOA8qL-LUQLClCGZIZTyDEMb0q1VTP3LHnL4hX6v5LOvkfaDw-eEBIokNOSr_MkOfQwJnDHbWd6YXsa4VSR2j7s8bNwpZ3JmI8qmN5nnVGYeSWyEn5yZGlL_NK-nABPts"
            }
        }
    }
}'
