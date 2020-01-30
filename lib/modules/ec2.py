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
            for instance in page['Reservations']:
                ids.append(instance['InstanceId'])

        return ids

    def list_resources(self):
        pass