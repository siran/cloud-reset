from ..BaseResource import BaseResource
import boto3

class Resource(BaseResource):
    name = 'ec2'
    type = 'ec2'

    def get_resources(self):
        client = boto3.client(self.type)
        paginator = client.get_paginator('describe_instances')
        ids = []
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for instance in reservation["Instances"]:
                    if instance.get('InstanceId'):
                        ids.append(instance['InstanceId'])

        return ids

    def list_resources(self):
        # ids = self.get_resources()
        # print(ids)
        pass

    def delete_resources(self):
        pass