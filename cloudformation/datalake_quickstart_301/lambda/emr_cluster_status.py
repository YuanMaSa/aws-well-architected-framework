"""
This module is the main script of EMR status fetching
"""
import os
import logging
import json
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger("status_handler")
logger.setLevel(logging.INFO)
logger.info('Loading function')

emr = boto3.client('emr')
sns = boto3.client('sns')

sns_topic = os.environ['SnsTopic']

def lambda_handler(event, context):
    """
    get the status from emr cluster
    """
    logger.info(event["emrInfo"])

    try:
        response = emr.describe_cluster(ClusterId=event["emrInfo"]["cluster_id"])
        logger.info(f"Response: \n{response}")

        cluster_state = response['Cluster']['Status']['State']
        logger.info(f"Cluster state: {cluster_state}")

        if cluster_state == 'RUNNING':
            # job is running
            logger.info("Sending running cluster notification to SNS topic")
            message = "EMR cluster " + event["emrInfo"]["cluster_id"]  + " is in running state "
            sns.publish(Message=message, TopicArn=sns_topic)
            output = 'RUNNING'

        elif cluster_state in ["BOOTSTRAPPING", "STARTING"]:
            # still not running
            logger.info("cluster is still BOOTSTRAPPING/STARTING")
            output = 'BOOTSTRAPPING/STARTING/WAITING'

        elif cluster_state == 'WAITING':
            logger.info("cluster is too fast to reach WAITING state may occur some error")
            output = 'FAILED'

        elif cluster_state in ["TERMINATING", "TERMINATED", "TERMINATED_WITH_ERRORS"]:
            # error occur
            logger.info("Sending error notification to SNS topic")
            message = "Failed EMR cluster " + event["emrInfo"]["cluster_id"]  + \
                " is in terminating / terminated state "
            sns.publish(Message=message, TopicArn=sns_topic)
            output = 'FAILED'
        else:
            output = 'FAILED'

        return output

    except ClientError as err:
        logger.error("The error occurred when getting the status of EMR cluster")
        logger.exception(err)
