"""
Delete resources as listed in a YAML file

Usage:
```
python delete_resources.py -f <resources.yml>
```

Example of `example.yml` file:
```
ec2:
    tags:
        Name: Test
```

Executing `python delete_resources.py -f example.yml` would delete all EC2 instances with tag `Name=Test`
"""

import argparse
import sys

from lib import AWSResetAccount #import AWSResetAccount
#import re
#from pprint import pprint


def get_args():
    parser = argparse.ArgumentParser(description='Description')

    parser.add_argument("-f", "--file", default=None, required=True,
                    help="Specify YAML file where resources are to be processed.")

    parser.add_argument("-x", "--execute", default=False, action='store_true',
                    help="Turn off dryrun flag.")

    parser.add_argument("-d", "--debug_options", action='store_true',
                    help="Debug options passed and exit.")

    args = parser.parse_args()

    # if not any(vars(args).values()):
    #     parser.parse_args(['--help'])
    #     # parser.error('No arguments provided.')

    if args.debug_options:
        print(args)
        sys.exit()

    return args

def main(config_file):
    aws_reset_account = AWSResetAccount.AWSResetAccount(config_file)
    aws_reset_account.dry_run = args.execute == False
    aws_reset_account.delete_resources()
    # aws_reset_account.delete_resources_by_type('ec2')


if __name__ == "__main__":
    args = get_args()
    config_file = args.file
    main(config_file)