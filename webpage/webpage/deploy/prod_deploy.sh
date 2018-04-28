#!/bin/bash
ansible-playbook -vvvv ./deploy.yml --private-key=~/.ssh/do_deploy -u deployer -i ./hosts
