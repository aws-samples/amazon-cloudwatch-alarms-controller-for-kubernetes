""" unit tests for cloudwatch alarms operator. """

from unittest.mock import patch
import sys
import os
import cwoperator.helpers.obj_parser as parser
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "src"))

def test_successfull_alarm_body_generation():
    """ test the creation of a cloudwatch alarm """

    spec = {
        "EvaluationPeriods": 4,
        "DatapointsToAlarm": 2,
        "ComparisonOperator": "LessThanLowerOrGreaterThanUpperThreshold",
        "ThresholdMetricId": "ad1",
        "Metrics": [
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
    expected_response = {
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
    return_value = parser.build_alarm_body(body, spec)
    assert expected_response == return_value

def test_successfull_alarm_body_generation():
    """ test the creation of a cloudwatch alarm """

    spec = {
        'AlarmRule' : 'someRule'
    }

    body = {
        "metadata": {
            "name": "test",
            "namespace": "kube-system"
        }
    }
    expected_response = {
        'AlarmRule' : 'someRule',
        'AlarmDescription': 'kube-system-test: Alarm Made by K8s Cloudwatch Adapter',
        'AlarmName': 'kube-system-test',
        'ActionsEnabled': True
    }
    return_value = parser.build_composit_alarm_body(body, spec)
    assert expected_response == return_value