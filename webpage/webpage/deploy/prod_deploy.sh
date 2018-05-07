#!/bin/bash
ansible-playbook -v ./deploy.yml --private-key=~/.ssh/do_deploy -u deployer -i ./hosts
