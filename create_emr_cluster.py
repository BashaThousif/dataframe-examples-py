import boto3


def lambda_handler(event, context):

    client = boto3.client('emr',  region_name="eu-west-1")

    instances = {
        'MasterInstanceType': 'm3.xlarge',
        'SlaveInstanceType': 'm3.xlarge',
        'InstanceCount': 2,
        'InstanceGroups': [],
        'Ec2KeyName': 'test',
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False,
        'Ec2SubnetId': 'subnet-076d7361',
        'EmrManagedMasterSecurityGroup': 'sg-079f080de0b7edc31',
        'EmrManagedSlaveSecurityGroup':  'sg-06693caa91f680db3'
    }

    configurations = [
        {
            'Classification': 'yarn-site',
            'Properties': {
                'yarn.resourcemanager.scheduler.class': 'org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler'
            },
            'Configurations': []
        },
        {
            "Classification": "spark-env",
            "Configurations": [
                {
                    "Classification": "export",
                    "Properties": {
                        "PYSPARK_PYTHON": "/usr/bin/python3"
                    }
                }
            ]
        }
    ]

    response = client.run_job_flow(
        Name='PySpark Cluster',
        LogUri='s3://thousif-test123/emr-logs',
        ReleaseLabel='emr-5.30.0',
        Instances=instances,
        Configurations=configurations,
        Steps=[],
        BootstrapActions=[],
        Applications=[
            {'Name': 'Spark'},
            {'Name': 'Zeppelin'},
            {'Name': 'Ganglia'}
        ],
        VisibleToAllUsers=True,
        ServiceRole='EMR_DefaultRole',
        JobFlowRole='EMR_EC2_DefaultRole',
        AutoScalingRole='EMR_AutoScaling_DefaultRole',
        EbsRootVolumeSize=30
    )
    return response["JobFlowId"]
