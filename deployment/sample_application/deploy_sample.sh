#!/bin/bash

QUEUE=`aws sqs list-queues --queue-name-prefix cloudwatch_test_queue`

if [ -z "$QUEUE" ]
then
  echo "Queue does not exist. Creating Now"
  aws sqs create-queue --queue-name cloudwatch_test_queue
fi

sed -i '' "s~OTLP_TEST_PRODUCER~$OTLP_TEST_PRODUCER~" deployment/sample_application/deployment.yml
sed -i '' "s~OTLP_TEST_CONSUMER~$OTLP_TEST_CONSUMER~" deployment/sample_application/deployment.yml

kubectl apply -f deployment/sample_application/deployment.yml
