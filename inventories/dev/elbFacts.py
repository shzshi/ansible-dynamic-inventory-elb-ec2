#!/usr/bin/env python

'''
custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
import string
import boto3 
import boto3.session

try:
    import json
except ImportError:
    import simpleJson as json

class AnsibleInventoryELB(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()
        
        # default inventory list dist
        self.myinventorydist = {'_meta':{'hostvars':{}}}

        if self.args.list:
            self.inventory = self.get_inventory()
        elif self.args.host:
            self.inventory = self.empty_inventory()
        else:
            self.inventory = self.empty_inventory()

        #print self.inventory
        print json.dumps(self.inventory);

    def get_inventory(self):

        # hard code the ELB name, but we can pass this as environment variable as well.
        elbName = "my-test-elb"
        hostNames = []
        elbList = self.get_client('elb')
        ec2 = self.get_resource('ec2')

        descBalc = elbList.describe_load_balancers()

        for myelb in descBalc['LoadBalancerDescriptions']:
            
            lSet2 = myelb['LoadBalancerName']

            if elbName == lSet2 :
                for ec2Id in myelb['Instances']:
                    running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']},{'Name': 'instance-id','Values': [ec2Id['InstanceId']]}])
                    for instance in running_instances:
                        hostNames.append(instance.public_dns_name)

                hostaddress = '","'.join(map(str, hostNames))

                self.myinventorydist["all"]={"hosts": hostNames}
                self.myinventorydist["all"]["vars"]={"ansible_user": "ec2-user"}

                self.create_hostvars_string(hostNames)

                return self.myinventorydist
    
    def empty_inventory(self):
        return {'_meta':{'hostvars':{}}}
    
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true', help='Ansible inventory of all')
        parser.add_argument('--host', action = 'store', help='Ansible inventory for particular host')
        self.args = parser.parse_args()

    def get_client(self, service):
        return boto3.client(
            service,
            region_name='us-east-1'
        )
    
    def get_resource(self, service):
        return boto3.resource(
            service,
            region_name='us-east-1'
        )

    def create_hostvars_string(self, hostNames):
        for item in hostNames:
            self.myinventorydist["_meta"]["hostvars"][item]={"variable_name": "value"}

AnsibleInventoryELB()