#!/bin/sh

: '
check the health of the https://geek.zone
try for 10 times with a interval of 10 seconds
at the end of the 10th time, trigger the API to spin up the AZURE Infra in the CircleCI
0-aws  
1-azure
Need to implement the trigger mechanism once the AWS is spic and span 
'
export CIRCLECI_TOKEN=$(echo ${CIRCLECI_TOKEN})

httpUrl="https://geek.zone"
rep=$(sudo curl -s -o /dev/null -w "%{http_code}"  $httpUrl)

i=0
result=0

if [ $rep == 200 ]
then
  echo " The website is healthy"
else  
  while [ i -le 10]
  do
  (( i++ ))
  sleep 10
  rep=$(sudo curl -s -o /dev/null -w "%{http_code}"  $httpUrl)

  if [ $rep == 200 ]
     exit 0
  elif [ i -ge 10 ]
      sudo curl -u ${CIRCLECI_TOKEN}: -X POST --header "Content-Type: application/json" -d '{
        "branch": "${CIRCLE_BRANCH}",
        "parameters": {     
        "deploy_switcher_infra_aws": false,
        "deploy_switcher_infra_azure": true,     
        "run_infra_build": false
        }
      }' https://circleci.com/api/v2/project/gh/GeekZoneHQ/web/pipeline
  fi
  done
fi




