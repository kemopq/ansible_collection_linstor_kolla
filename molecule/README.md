# Testing Ansible Collection with molecule(docker) and without it
### Prepare testing environment
#### Install and run docker
On Ubuntu18.04/20.04:
```
sudo apt update
sudo apt install docker.io
sudo service docker start
```
On other OS, search the net.
#### Install molecule
```
pip3 install molecule[docker,lint]
```
Package is installed on _~/.local/bin_ folder. Check if installation was OK:
```
molecule --version
molecule 3.2.0 using python 3.8
    ansible:2.10.3
    delegated:3.2.0 from molecule
    docker:0.2.4 from molecule_docker
```

#### Configure lint
Lint can be configured in _~/.config/yamllint/config file_.  
I changed a few default options (max line length, comment identation)
```
# It extends the default conf by adjusting some options.

extends: default

rules:
  comments-indentation: disable  # don't bother me with this rule
  line-length:
    max: 150
    level: warning
```

#### Add testing scenario
Go to the collection folder and run:  
```
molecule init scenario --driver-name=docker [<scenario_name>]
```
First created scenario is named default. For next scenarios the name should be provided. 
A folder molecule/default is created. On that folder three files are created:  
_molecule.yml_   #description of testing environment  
_converge.yml_   #testing playbook  
_verify.yml_     #verification playbook  

#### Make molecule configuration
Add some configuration data to  _molecule.yml_ file (see the _molecule.yml_ in this collection).  
- Add yamllint and ansible-lint test (_lint_ section)
- Set molecule testing instances - docker containers (_platforms_ section)
- Set additional parameter to _provisioner_ section

#### Prepare main ansible playbook
The _converge.yml_ is your main testing playbook. Import collection's roles to this 
playbook. Plugins can also be called.

#### Prepare verify ansible playbook (not required)
The _verify.yml_ is your verify playbook. It is run after main playbook and checks if 
the result is OK. (e.g. you can check if web server is running if the purpose of the collection 
is to install, configure and start this server.)  

#### Add collection path to ansible configuration
Put additional collections_path to ansible.cfg
```
[defaults]
# Paths to search for collections, colon separated
collections_path = ./../../..
```

### Make tests
#### Run molecule actions
```
molecule create           #run molecule testing instances  (e.g. molecule testing containers)
molecule list             #list molecule testing instances
molecule destroy          #destroy molecule testing instances
molecule login [-h name]  #login to testing instance (name should be provided, if there are more then one instance)
molecule lint             #run lint testing
molecule converge         #run main testing playbook, if instances are already created, the playbook is run on those instances
molecule verify           #run verify playbook
molecule test             #run the whole test (create new instances, run lint testing, run main playbook twice, run verify playbook)
```

#### Testing without molecule
Some additional tests can be done using the same playbooks.
```
yamllint .
ansible-playbook --syntax-check -i localhost, molecule/default/converge.yml
ansible-lint molecule/default/converge.yml
ansible-playbook --check -i localhost, molecule/default/converge.yml
```
