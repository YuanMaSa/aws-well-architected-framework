"""
This module is the main script of Athena query
"""
import os
import logging
import boto3
from botocore.exceptions import ClientError


msg_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(format=msg_format, datefmt='%Y-%m-%d %H:%M:%S')
formatter = logging.Formatter(msg_format)
logger = logging.getLogger("lab_logger")
logger.setLevel(logging.INFO)

ecr_repo = os.environ["REPO_NAME"]
region = os.environ["REGION"]
ecr = boto3.client('ecr', region_name=region)

def main():
    """
    Main function
    """
    try:
        logger.info("main function start")

        get_image = ecr.batch_get_image(
            repositoryName=ecr_repo,
            imageIds=[{'imageTag': 'latest'}]
        )
        if len(get_image["images"]) > 0:
            info = get_image["images"]
            logger.info(f"list the image information\n{info}")

            for item in get_image["images"]:
                registry_id = item["registryId"]
                image_id = item["imageId"]
                image_manifest = item["imageManifest"]
                logger.info(f"Registry Id: {registry_id}")
                logger.info(f"Image Id: {image_id}")
                logger.info(f"Image Manifest: {image_manifest}")

        logger.info("main function run finish")

    except ClientError as error:
        logger.error("The error occurred when running main function")
        logger.exception(error)


if __name__ == '__main__':
    main()
    logger.info("############################################")
    logger.info("Data & Analytic Team")
    logger.info("############################################")
    logger.info("Happy Coding")
    logger.info("############################################")
    logger.info("Keep Samuelizing")
    logger.info("############################################")
