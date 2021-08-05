aws ecr-public get-login-password | docker login --username AWS --password-stdin public.ecr.aws

CW_ALARM_OPERATOR=`aws ecr-public create-repository \
    --repository-name cw-alarm-operator | jq ".repository.repositoryUri" | sed -e 's/^"//' -e 's/"$//'`

OTLP_TEST_PRODUCER=`aws ecr-public create-repository \
    --repository-name otlp-test-producer | jq ".repository.repositoryUri" | sed -e 's/^"//' -e 's/"$//'`

OTLP_TEST_CONSUMER=`aws ecr-public create-repository \
    --repository-name otlp-test-consumer | jq ".repository.repositoryUri" | sed -e 's/^"//' -e 's/"$//'`

echo $CW_ALARM_OPERATOR
echo $OTLP_TEST_PRODUCER
echo $OTLP_TEST_CONSUMER

export CW_ALARM_OPERATOR=$CW_ALARM_OPERATOR
export OTLP_TEST_PRODUCER=$OTLP_TEST_PRODUCER
export OTLP_TEST_CONSUMER=$OTLP_TEST_CONSUMER

docker build -t $CW_ALARM_OPERATOR .
docker push $CW_ALARM_OPERATOR

docker build -t $OTLP_TEST_PRODUCER sample/producer
docker push $OTLP_TEST_PRODUCER

docker build -t $OTLP_TEST_CONSUMER sample/consumer
docker push $OTLP_TEST_CONSUMER