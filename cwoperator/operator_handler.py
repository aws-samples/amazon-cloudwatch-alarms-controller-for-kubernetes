"""Create, Update and Delete cloudwatch alarms from K8s manifests"""

import os
import sys
import kopf
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, ".."))
from cwoperator.helpers import cloudwatch
from cwoperator.helpers import obj_parser

logging.basicConfig(level=logging.INFO)

@kopf.on.update('cw.aws.com', 'v1', 'cloudwatchmetricalarm')
@kopf.on.create('cw.aws.com', 'v1', 'cloudwatchmetricalarm')
def create_fn(body, spec, **kwargs):
    """ create and update action
    Build payload for boto3 put metric alarm call. """
    logging.info("body: %s", str(body))
    logging.info("spec: %s", str(spec))
    alarm = obj_parser.build_alarm_body(body, spec)
    cloudwatch.put_cloudwatch_alarm(alarm)
    alarm_name = alarm["AlarmName"]
    return {'message': f"{alarm_name} created"}

@kopf.on.delete('cw.aws.com', 'v1', 'cloudwatchmetricalarm')
@kopf.on.delete('cw.aws.com', 'v1', 'cloudwatchcompositalarm')
def delete(body, spec, **kwargs):
    """ delete action """
    logging.info("body: %s", str(body))
    logging.info("spec: %s", str(spec))
    alarm_name = f"{body['metadata']['namespace']}-{body['metadata']['name']}"
    cloudwatch.delete_alarm(alarm_name)
    return {'message': f"{alarm_name} deleted"}

@kopf.on.update('cw.aws.com', 'v1', 'cloudwatchcompositalarm')
@kopf.on.create('cw.aws.com', 'v1', 'cloudwatchcompositalarm')
def create_composit_fn(body, spec, **kwargs):
    """ create and update action
    Build payload for boto3 put composit alarm call. """
    logging.info("body: %s", str(body))
    logging.info("spec: %s", str(spec))
    alarm = obj_parser.build_composit_alarm_body(body, spec)
    cloudwatch.put_cloudwatch_composit_alarm(alarm)
    alarm_name = alarm["AlarmName"]
    return {'message': f"{alarm_name} created"}
