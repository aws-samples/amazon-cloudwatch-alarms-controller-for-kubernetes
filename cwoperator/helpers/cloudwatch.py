import boto3
import botocore
import kopf

def cloudwatch_client(): # pragma: no cover
    """gets cloudwatch client. Here for unit testing"""
    return boto3.client('cloudwatch')

def put_cloudwatch_alarm(alarm):
    cloudwatch = cloudwatch_client()
    try:
        cloudwatch.put_metric_alarm(**alarm)
    except botocore.exceptions.ClientError as error:
        raise kopf.TemporaryError(f"boto client error occurred. Retry in 60s : {error}",
            delay=60) # pragma: no cover

    except botocore.exceptions.ParamValidationError as error:
        raise kopf.PermanentError(f"The parameters you provided are incorrect: {error}")

def put_cloudwatch_composit_alarm(alarm):
    cloudwatch = cloudwatch_client()
    try:
        cloudwatch.put_composite_alarm(**alarm)
    except botocore.exceptions.ClientError as error:
        raise kopf.TemporaryError(f"boto client error occurred. Retry in 60s : {error}",
            delay=60) # pragma: no cover

    except botocore.exceptions.ParamValidationError as error:
        raise kopf.PermanentError(f"The parameters you provided are incorrect: {error}")


def delete_alarm(alarm_name):
    cloudwatch = cloudwatch_client()
    try:
        cloudwatch.delete_alarms(
            AlarmNames=[
                f"{alarm_name}",
            ]
        )
    except Exception as exception: # pragma: no cover
        raise kopf.TemporaryError("error deleting occured. Retrying in 10s",
            delay=10) from exception
