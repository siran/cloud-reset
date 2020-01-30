import boto3

class Resource:
    name = 'kms'
    type = 'kms'

    def get_resources(self):
        client = boto3.client(self.type)
        resources = client.list_aliases()
        ids = []
        for resource in resources['Aliases']:
            # for instance in page['Reservations']:
                ids.append(resource['AliasArn'])

        return ids

    def list_resources(self):
        pass

