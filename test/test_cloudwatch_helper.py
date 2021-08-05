""" unit tests for cloudwatch alarms operator. """

from unittest.mock import patch
import sys
import os
import botocore
from botocore.stub import Stubber
import cwoperator.helpers.cloudwatch as cloudwatch

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "src"))

CW_CLIENT = botocore.session.get_session().create_client('cloudwatch')
CW_STUB = Stubber(CW_CLIENT)

@patch.object(cloudwatch, 'cloudwatch_client', return_value=CW_CLIENT)
def test_successfull_alarm_creation(cloudwatch_client):
    """ test the creation of a cloudwatch alarm """
    CW_STUB.add_response('put_metric_alarm', "")
    alarm = {
        'ActionsEnabled': True,
        'AlarmDescription': 'kube-system-test: Alarm Made by K8s Cloudwatch Adapter',
        'AlarmName': 'kube-system-test',
        'ComparisonOperator': 'LessThanLowerOrGreaterThanUpperThreshold',
        'DatapointsToAlarm': 2,
        'EvaluationPeriods': 4,
        'Metrics': [{'Id': 'm1',
            'MetricStat': {'Metric': {'Dimensions': [{'Name': 'ClusterName',
            'Value': 'mycluster'},
            {'Name': 'Serivce',
            'Value': 'kube-dns'},
            {'Name': 'Namespace',
            'Value': 'kube-system'}
        ],
            'MetricName': 'pod_cpu_utilization',
            'Namespace': 'ContainerInsights'},
            'Period': 10,
            'Stat': 'p95'},
            'ReturnData': True},
            {'Expression': 'ANOMALY_DETECTION_BAND(m1, 2)',
            'Id': 'ad1',
            'Label': 'pod_cpu_utilizatio (expected)',
            'ReturnData': True}
        ],
        'ThresholdMetricId': 'ad1'
    }

    with CW_STUB:
        return_value = cloudwatch.put_cloudwatch_alarm(alarm)
    assert None == return_value

@patch.object(cloudwatch, 'cloudwatch_client', return_value=CW_CLIENT)
def test_successfull_composit_alarm_creation(cloudwatch_client):
    """ test the creation of a composit cloudwatch alarm """
    CW_STUB.add_response('put_composite_alarm', "")
    alarm = {
        'ActionsEnabled': True,
        'AlarmDescription': 'kube-system-test: Alarm Made by K8s Cloudwatch Adapter',
        'AlarmName': 'kube-system-test',
        'AlarmRule' : 'someRule'
    }

    with CW_STUB:
        return_value = cloudwatch.put_cloudwatch_composit_alarm(alarm)
    assert None == return_value

@patch.object(cloudwatch, 'cloudwatch_client', return_value=CW_CLIENT)
def test_successfull_alarm_deletion(cloudwatch_client):
    """ test the deletion of a cloudwatch alarm """
    CW_STUB.add_response('delete_alarms', "")
    alarm = {
        'AlarmName': 'kube-system-test'
    }

    with CW_STUB:
        return_value = cloudwatch.delete_alarm(alarm)
    assert None == return_value
