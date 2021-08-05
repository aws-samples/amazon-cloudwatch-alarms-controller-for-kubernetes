""" unit tests for cloudwatch alarms operator. """

from unittest.mock import patch
import botocore
import sys
import os
from botocore.stub import Stubber
import kopf
import cwoperator.operator_handler as operator_handler

@patch.object(operator_handler, 'cloudwatch', return_value=None)
def test_successfull_create(cloudwatch):
    """ test the creation of a cloudwatch alarm """
    spec = {
        "evaluationPeriods": 4,
        "datapointsToAlarm": 2,
        "comparisonOperator": "LessThanLowerOrGreaterThanUpperThreshold",
        "thresholdMetricId": "ad1",
        "metrics": [
            {
                "Id": "m1",
                "ReturnData": True,
                "MetricStat": {
                    "Metric": {
                        "Namespace": "ContainerInsights",
                        "MetricName": "pod_cpu_utilization",
                        "Dimensions": [
                            {
                                "Name": "ClusterName",
                                "Value": "mycluster"
                            },
                            {
                                "Name": "Serivce",
                                "Value": "kube-dns"
                            },
                            {
                                "Name": "Namespace",
                                "Value": "kube-system"
                            }
                        ]
                    },
                    "Period": 10,
                    "Stat": "p95"
                }
            },
            {
                "Id": "ad1",
                "Label": "pod_cpu_utilizatio (expected)",
                "ReturnData": True,
                "Expression": "ANOMALY_DETECTION_BAND(m1, 2)"
            }
        ]
    }

    body = {
        "metadata": {
            "name": "test",
            "namespace": "kube-system"
        }
    }
    expected_response = {'message': "kube-system-test created"}
    return_value = operator_handler.create_fn(body, spec)
    assert expected_response == return_value

@patch.object(operator_handler, 'cloudwatch', return_value=None)
def test_successfull_alarm_deletion(cloudwatch):
    """ test the deletion of a cloudwatch alarm """
    body = {
        "metadata": {
            "name": "test",
            "namespace": "kube-system"
        }
    }
    spec = {

    }
    expected_response = {'message': "kube-system-test deleted"}

    return_value = operator_handler.delete(body, spec)
    assert expected_response == return_value
