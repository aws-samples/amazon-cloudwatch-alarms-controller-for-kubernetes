import logging

logging.basicConfig(level=logging.INFO)

def append_conditionally(key, value, alarm):
    """Add key to dictionary if key is in parent dictionary"""
    if value:
        alarm[key] = value
    return alarm


def build_alarm_body(body, spec, **kwargs):
    """ create and update action
    Build payload for boto3 put metric alarm call. """
    alarm = {}
    name = body['metadata']['name']
    namespace = body['metadata']['namespace']
    alarm_name = f"{namespace}-{name}"

    alarm["AlarmName"] = alarm_name
    alarm["AlarmDescription"] = f"{alarm_name}: Alarm Made by K8s Cloudwatch Adapter"
    alarm["ActionsEnabled"] = True

    alarm = append_conditionally("OkActions", spec.get('OkActions'), alarm)
    alarm = append_conditionally("AlarmActions", spec.get('AlarmActions'), alarm)
    alarm = append_conditionally("InsufficientDataActions",
                            spec.get('InsufficientDataActions'), alarm)
    alarm = append_conditionally("MetricName", spec.get('MetricName'), alarm)
    alarm = append_conditionally("Namespace", spec.get('CloudwatchMetricNamespace'), alarm)
    alarm = append_conditionally("Statistic", spec.get('Statistic'), alarm)
    alarm = append_conditionally("EtendedStatistic", spec.get('ExtendedStatistic'), alarm)
    alarm = append_conditionally("Dimensions", spec.get('Dimensions'), alarm)
    alarm = append_conditionally("Period", spec.get('Period'), alarm)
    alarm = append_conditionally("EvaluationPeriods", spec.get('EvaluationPeriods'), alarm)
    alarm = append_conditionally("DatapointsToAlarm", spec.get('DatapointsToAlarm'), alarm)
    alarm = append_conditionally("Threshold", spec.get('Threshold'), alarm)
    alarm = append_conditionally("ComparisonOperator", spec.get('ComparisonOperator'), alarm)
    alarm = append_conditionally("TreatMissingData", spec.get('TreatMissingData'), alarm)
    alarm = append_conditionally("EvaluateLowSampleCountPercentile",
                            spec.get('EvaluateLowSampleCountPercentile'), alarm)
    alarm = append_conditionally("Metrics", spec.get('Metrics'), alarm)
    alarm = append_conditionally("ThresholdMetricId", spec.get('ThresholdMetricId'), alarm)
    alarm = append_conditionally("Tags", spec.get('Tags'), alarm)

    logging.info("MetricAlarm: %s", alarm)

    return alarm

def build_composit_alarm_body(body, spec, **kwargs):
    """ create and update action
    Build payload for boto3 put metric alarm call. """
    alarm = {}
    name = body['metadata']['name']
    namespace = body['metadata']['namespace']
    alarm_name = f"{namespace}-{name}"

    alarm["AlarmName"] = alarm_name
    alarm["AlarmDescription"] = f"{alarm_name}: Alarm Made by K8s Cloudwatch Adapter"
    alarm["ActionsEnabled"] = True

    alarm = append_conditionally("OkActions", spec.get('OkActions'), alarm)
    alarm = append_conditionally("AlarmActions", spec.get('AlarmActions'), alarm)
    alarm = append_conditionally("InsufficientDataActions",
                            spec.get('InsufficientDataActions'), alarm)
    alarm = append_conditionally("AlarmRule", spec.get('AlarmRule'), alarm)
    alarm = append_conditionally("Tags", spec.get('Tags'), alarm)

    logging.info("CompositAlarm: %s", alarm)

    return alarm
