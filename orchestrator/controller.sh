#!/bin/bash

sshpass -p "TUC-2018" ssh -o StrictHostKeyChecking=no knos@10.20.4.80 'bash /home/knos/vibha/sarnet.sh; bash -l'

#echo TUC-2018 
