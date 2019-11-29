## About this lab

### AWS Data Lake quickstart

This lab using a Cloudformation Stack to generate the following items:
* v
* 
*

**This lab using the following datasets from Kaggle and NYC gov**
* https://www.kaggle.com/fivethirtyeight/uber-pickups-in-new-york-city

    ![kaggle_uber.png](./img/kaggle_uber.png)
* https://www.kaggle.com/selfishgene/historical-hourly-weather-data#city_attributes.csv

    ![kaggle_weather.png](./img/kaggle_weather.png)
* https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

    ![nyc_gov.png](./img/nyc_gov.png)


### Prerequisites

* You must have an AWS account and an IAM user with sufficient permissions to interact with the AWS Management Console

* Create an EC2 key pair for the bastion if you do not have one in this AWS Region, create it before continuing
    * [How to create EC2 key pairs](https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

* Download the CloudFormation stack **datalake_qs.yml**

### CloudFormation Deployment

* On the service menu, click **CloudFormation**
* For **Prepare template**, choose **Template is ready**
* For **Specify template**, select **Upload a template file** and select **Choose file**.
* Choose the **datalake_qs.yml**
* Click **Next**
* Enter the values in each Parameters and create the stack.

### Clean-Up Operation Procedures

* Find the S3 BucketFor Redshift which was created by CloudFormation template.
    * (e.g., redshift-spectrum-bucket-ver6689)

* Delete all object in the bucket and make sure the bucket is empty

![bucket_deletion.png](./img/bucket_deletion.png)

* On the service menu, click **CloudFormation**
* On AWS CloudFormation console make sure that the region is where you created the stack
* Click **Delete** to remove the stack along with all resources

* **The deletion time will take 10 mins to 20 mins depends on the size of your Redshift cluster**

### Lab References