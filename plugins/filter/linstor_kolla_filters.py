############################################
# linstor_kolla collection's filter plugins
############################################

# filter: linstor_node_list
# Prepare list of linstor cluster nodes from "linstor node list" JSON output
def filter_node_list(in_list):
    node_list = []
    print(type(in_list))
    if type(in_list) is list:
        for node in in_list[0]['nodes']:
            node_list.append(node['name'])
    return node_list


# filter: linstor_pool_list
# Prepare list of linstor pools from "linstor storage-pool list" JSON output
def filter_pool_list(in_list):
    pool_list = []
    if type(in_list) is list:
        for pool in in_list[0]['stor_pools']:
            pool_list.append(pool['stor_pool_name'])
    return pool_list


# filter module
class FilterModule(object):
    def filters(self):
        return {
                'linstor_node_list': filter_node_list,
                'linstor_pool_list': filter_pool_list
        }
