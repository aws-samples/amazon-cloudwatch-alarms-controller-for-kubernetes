# Amazon cloudwatch alarms controller for kubernetes

This repo is a custom controller for kubernetes that when installed in a cluster grantes the cluster access to the Cloudwatch metrics alarms api. Thus, allowing developers to define alarms from their kubernetes manifests.

## Installation

There are some example manifests in the examples folder that you can utilize.

### Testing

To run unit tests you can run the following commands.

`docker-compose build test-coverage`
`docker-compose run test-coverage`

### Note

The definition of the service account in the example will require you to make an IAM role for your service account according to the [documentation](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) ensuring that the policy on the role has cloudwatch access. Then you will need to update the section of the cloudwatch_alarms_operator.yml file in the examples folder to reference the ARN of the role made in the previous step.

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: null
  name: cloudwatchalarm-controller
  namespace: kube-system
  labels:
    app: cloudwatchalarm-controller
  annotations:
    eks.amazonaws.com/role-arn: {{THE ROLE YOU CREATED FOR THE CONTROLLER}}
```

You will also need to push changes to gitlab so that they can be built and published. Then update the reference to the image build on you feature branch for testing.

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudwatchalarm-controller
  namespace: kube-system
  labels:
    app: cloudwatchalarm
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: cloudwatchalarm
      role: operator
  template:
    metadata:
      labels:
        app: cloudwatchalarm
        role: operator
      annotations:
        prometheus.io/scrape: 'false'
    spec:
      serviceAccountName: cloudwatchalarm-controller
      containers:
        - name: cloudwatchalarm
          image: {{WHEREVER YOU PUSH YOUR IMAGE}}
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
              protocol: TCP
          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "500Mi"


## Example alarm definition

```yaml
---
apiVersion: cw.aws.com/v1
kind: cloudwatchmetricalarm
metadata:
  namespace: kube-system
  name: test-kube-dns-alarm
spec:
  EvaluationPeriods: 4
  DatapointsToAlarm: 2
  ComparisonOperator: LessThanLowerOrGreaterThanUpperThreshold
  ThresholdMetricId: ad1
  AlarmActions:
    - {{ ARN_FOR_ACTION_RESOURCE }}
  Metrics:
    - Id: "m1"
      ReturnData: true
      MetricStat:
        Metric:
          Namespace: ContainerInsights
          MetricName: pod_cpu_utilization
          Dimensions:
            - Name: ClusterName
              Value: {{CLUSTER_NAME}}
            - Name: Serivce
              Value: kube-dns
            - Name: Namespace
              Value: kube-system
        Period: 10
        Stat: p95
    - Id: ad1
      Label: pod_cpu_utilization (expected)
      ReturnData: true
      Expression: ANOMALY_DETECTION_BAND(m1, 2)

---
apiVersion: cw.aws.com/v1
kind: cloudwatchmetricalarm
metadata:
  namespace: kube-system
  name: test-cluster-autoscaler-alarm
spec:
  EvaluationPeriods: 4
  DatapointsToAlarm: 2
  ComparisonOperator: LessThanLowerOrGreaterThanUpperThreshold
  ThresholdMetricId: ad1
  AlarmActions:
    - {{ ARN_FOR_ACTION_RESOURCE }}
  Metrics:
    - Id: "m1"
      ReturnData: true
      MetricStat:
        Metric:
          Namespace: ContainerInsights
          MetricName: pod_cpu_utilization
          Dimensions:
            - Name: ClusterName
              Value: {{CLUSTER_NAME}}
            - Name: Serivce
              Value: cluster-autoscaler
            - Name: Namespace
              Value: cluster-autoscaler
        Period: 10
        Stat: p95
    - Id: ad1
      Label: pod_cpu_utilization (expected)
      ReturnData: true
      Expression: ANOMALY_DETECTION_BAND(m1, 2)

---
apiVersion: cw.aws.com/v1
kind: cloudwatchcompositalarm
metadata:
  namespace: kube-system
  name: test-composit-alarm
spec:
  AlarmRule: ALARM("kube-system-test-cluster-autoscaler-alarm") OR ALARM("kube-system-test-kube-dns-alarm")
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
