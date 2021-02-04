README.linstor_kolla  
# kemopq.linstor_kolla collection
Collection for creating Linstor cluster and integrate it to kolla Openstack.  
https://www.linbit.com/linstor/

### Installing collection  
Install this collection locally:
```
ansible-galaxy collection install kemopq.linstor_kolla -p ./collections
```
_./collections_ folder should be included to _collections_path_ parameter in ansible configuration file. See:
https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-configuration-settings-locations

### Using collection  
Roles and module can be used on your ansible playbook. It can be  referenced by its fully qualified collection name (FQCN):
```
- name: Prepare linstor nodes
  hosts: linstor_all
  gather_facts: 'yes'

  collections:
    - kemopq.linstor_kolla
  tasks:
    - name: "Include linstor_nodes role"
      import_role:
        name: "linstor_nodes"
      tags:
        - lnodes

- name: Setup linstor cluster
  hosts: linstor_controller[0]
  gather_facts: 'no'

  collections:
    - kemopq.linstor_kolla

  tasks:
    - name: "Include linstor_cluster role"
      import_role:
        name: "linstor_cluster"
      tags:
        - lcluster

- name: Prepare Cinder configuration on Openstack deployment server
  hosts: deployment_srv
  gather_facts: 'no'

  collections:
    - kemopq.linstor_kolla

  tasks:
    - name: "Include openstack_config role"
      import_role:
        name: "openstack_config"
      tags:
        - osconfig

- name: Prepare Openstack Cinder nodes
  hosts: cinder_storage
  gather_facts: 'no'

  collections:
    - kemopq.linstor_kolla

  tasks:
    - name: "Include openstack_nodes role"
      import_role:
        name: "openstack_nodes"
      tags:
        - osnodes
```

### Configuration parameters
Template of configuration file is in config folder. It's well commented. The configuration file has three parts:
- drbd configuration (most parameters can have default values, check only drbd_volumes)
- linstor cluster configuration   
- kolla openstack configuration

### Inventory
Template of inventory file is in config folder. There are three types of server:
- deployment_srv => the server where kolla ansible playbooks run
- linstor_controller => linstor controller nodes
- linstor_satellite => linstor satellite nodes
- cinder_storage => nodes, which will play the role of cinder storage on Linstor cluster; usually on these nodes Linstor controller runs  
A node can be in controller and satellite group, if it has both roles.

### Running your playbook
When running your playbook a path to configuration file should be provided. Additionaly a parameter _linstor_kolla_action_ parameter should be set. Possible values are:
- 'deploy': linstor cluster is deployed and integrated to kolla Openstack
- 'destroy': linstor cluster is destroyed
```
ansible-playbook  -i localhost, -e linstor_kolla_action=[deploy/destroy] -e "@<your_config_file>.json" <your_playbook>.yml
```

### Integration with kolla Openstack
- deploy Openstack cloud with kolla-ansible playbooks
- prepare Linstor cluster with this ansible collection (Caveat: ensure passwordless ssh to cloud nodes)
- run kolla-ansible playbook with reconfigure option

### Basic test
On openstack client host:
```
source admin-openrc.sh
openstack volume type create linstor
openstack volume type set linstor --property volume_backend_name=linstor
openstack volume create --type linstor --size 1 --availability-zone nova linstor-testvol
openstack volume list
```

On cinder controller:
```
docker run -it --rm -e LS_CONTROLLERS="192.168.100.11" drbd.io/linstor-client resource list
```

### Testing with molecule
Not prepaired yet
