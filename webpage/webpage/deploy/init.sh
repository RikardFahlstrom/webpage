#!/bin/bash
ansible-playbook -vvvv ./init_config.yml --private-key=~/.ssh/do_deploy -u root -i ./hosts
