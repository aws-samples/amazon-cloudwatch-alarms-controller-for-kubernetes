#!/bin/bash

QUEUE=`aws sqs get-queue-url --queue-name cloudwatch_test_queue --query QueueUrl | tr -d '"'`

aws sqs delete-queue --queue-url $QUEUE

kubectl delete -f deployment/sample_application/deployment.yml