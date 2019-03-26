
Dynamic Inventory for EC2 instances attached to ELB

Pre-requisite : 

- An AWS account (free-tier should be fine) 
- A classic ELB with at-least one EC2 instance attached to it.
- Need to export session and secret keys for python script to execute or it can be picked up from the ~/.aws/credentials

   export AWS_ACCESS_KEY_ID=<my_access_key>

   export AWS_SECRET_ACCESS_KEY=<my_secret_key>

- And most important you need to make sure you have pass host variable ansible_user for ansible to connect to ec2 instances. eg. {"ansible_user": "ec2-user"}

How to execute : 

ansible-playbook -i inventories/dev/elbFacts.py ./playbooks/myPlay.yml
