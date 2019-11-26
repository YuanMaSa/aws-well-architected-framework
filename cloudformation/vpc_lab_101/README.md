## About this lab

### VPC with private and public subnets in two Availability Zones

This lab is a fundamental VPC setup, therefore, it does not include any advanced infrastructure or complex network configuration

![Diagram-vpc_lab.png](./cloudformation/vpc_lab_101/img/Diagram-vpc_lab.png)

### CloudFormation Deployment
* On the service menu, click **CloudFormation**
* For **Prepare template**, choose **Template is ready**
* For **Specify template**, select **Upload a template file** and select **Choose file**.
* Choose the **vpc.yml**
* Click **Next**
* Enter the values in each Parameters and create the stack.
* Enter the parameters for **Prefix configuration** and **VPC configuration**
    * Make sure that **Prefix Name** must only contain lowercase letters and numbers or underscore (_)
    * Make sure the input parameters must match the pattern

![cf.png](./cloudformation/vpc_lab_101/img/cf.png)

* After entered every parameter and the stack name, click **Next**
* On **Configure stack options** page, add a stack-level tag with **Project** and **VPC Lab** as key and value

![tag.png](./cloudformation/vpc_lab_101/img/tag.png)

* Click **Next**
* Click **Create Stack**
* CloudFormation will start building all resources 


### Clean-Up Operation Procedures

* On the service menu, click **CloudFormation**
* On AWS CloudFormation console make sure that the region is where you created the stack
* Click **Delete** to remove the stack along with all resources

### References
More illustrations of VPC design 
* [AWS Architecture Blog](https://aws.amazon.com/tw/blogs/architecture/one-to-many-evolving-vpc-design/)