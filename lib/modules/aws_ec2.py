from ..BaseResource import BaseResource
import boto3

class Resource(BaseResource):
    name = 'aws_ec2'
    type = 'ec2'
    client = None
    dry_run = True
    ids = []
    resources = []

    def __init__(self):
        self.client = boto3.client(self.type)

    def get_resources(self):
        client = self.client
        paginator = client.get_paginator('describe_instances')
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation["Instances"]:
                    if instance.get('InstanceId'):
                        self.ids.append(instance['InstanceId'])
                        self.resources.append({
                            "Id": instance['InstanceId'],
                            "Tags": instance.get('Tags'),
                        })

        return self.ids

    def list_resources(self):
        self.get_resources()
        pprint(self.ids)
        pass

    def delete_resources(self, ids):
        """ delete resources specified by ids list"""
        client = self.client
        if self.dry_run:
            print('dry_run flag set')
        try:
            response = client.terminate_instances(
                InstanceIds=ids,
                DryRun=self.dry_run
            )
            return True
        except Exception as error:
            if error.response.get('Error').get('Code') == 'DryRunOperation':
                pass
            else:
                raise
