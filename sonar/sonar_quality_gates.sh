#!/bin/bash 

set -eo pipefail
REPORT_PATH=".scannerwork/report-task.txt"
CE_TASK_ID_KEY="ceTaskId="

SONAR_INSTANCE="https://sonarcloud.io"
SLEEP_TIME=5

# get the compute engine task id
ce_task_id=$(cat $REPORT_PATH | grep $CE_TASK_ID_KEY | cut -d'=' -f2)
echo "Using task id of ${ce_task_id}"

if [ -z "$ce_task_id" ]; then
   echo "No task id found"
   exit 1
fi

# grab the status of the task
# if CANCELLED or FAILED, fail the Build
# if SUCCESS, stop waiting and grab the analysisId
wait_for_success=true

while [ "${wait_for_success}" = "true" ]
do
  ce_status=$(curl -s -u "${SONAR_AUTH_TOKEN}": "${SONAR_INSTANCE}"/api/ce/task?id=${ce_task_id} | jq -r .task.status)

  echo "Status of SonarQube task is ${ce_status}"

  if [ "${ce_status}" = "CANCELLED" ]; then
    echo "SonarQube Compute job has been cancelled - exiting with error"
    exit 504
  fi

  if [ "${ce_status}" = "FAILED" ]; then
    echo "SonarQube Compute job has failed - exit with error"
    exit 500
  fi

  if [ "${ce_status}" = "SUCCESS" ]; then
    wait_for_success=false
  fi

  sleep "${SLEEP_TIME}"

done

ce_analysis_id=$(curl -s -u $SONAR_AUTH_TOKEN: $SONAR_INSTANCE/api/ce/task?id=$ce_task_id | jq -r .task.analysisId)
echo "Using analysis id of ${ce_analysis_id}"

# get the status of the quality gate for this analysisId
qg_status=$(curl -s -u $SONAR_AUTH_TOKEN: $SONAR_INSTANCE/api/qualitygates/project_status?analysisId="${ce_analysis_id}" | jq -r .projectStatus.status)
echo "Quality Gate status is ${qg_status}"

if [ "${qg_status}" != "OK" ]; then
  echo "Quality gate is not OK - exiting with error"
  exit 1
fi