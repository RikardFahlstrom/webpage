#!/bin/bash
ansible-playbook -vvv ./deploy.yml --private-key=~/.ssh/do_deploy -u deployer -i ./hosts
