#!/usr/bin/python
#
# Copyright (c) 2020  haiyuazhang <haiyzhan@micosoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from types import LambdaType
from os import path
__metaclass__ = type


DOCUMENTATION = '''
---
module: azure_rm_openshiftmanagedcluster
version_added: '1.2.0'
short_description: Manage Azure Red Hat OpenShift Managed Cluster instance
description:
    - Create, update and delete instance of Azure Red Hat OpenShift Managed Cluster instance.
options:
    resource_group:
        description:
            - The name of the resource group.
        required: true
        type: str
    name:
        description:
            - Resource name.
        required: true
        type: str
    location:
        description:
            - Resource location.
        required: true
        type: str
    cluster_profile:
        description:
            - Configuration for OpenShift cluster.
        type: dict
        default: {}
        suboptions:
            pull_secret:
                description:
                    - Pull secret for the cluster (immutable).
                type: str
            domain:
                description:
                    - The domain for the cluster (immutable).
                type: str
            cluster_resource_group_id:
                description:
                    - The ID of the cluster resource group (immutable).
                type: str
            version:
                description:
                    - The Openshift version (immutable).
                type: str
            fips_validated_modules:
                description:
                    - If FIPS validated crypto modules are used
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Enabled
    service_principal_profile:
        description:
            - service principal.
        type: dict
        suboptions:
            client_id:
                description:
                    - Client ID of the service principal (immutable).
                required: true
                type: str
            client_secret:
                description:
                    - Client secret of the service principal (immutable).
                required: true
                type: str
    network_profile:
        description:
            - Configuration for OpenShift networking (immutable).
        type: dict
        default: {'pod_cidr' : '10.128.0.0/14', 'service_cidr' : '172.30.0.0/16'}
        suboptions:
            pod_cidr:
                description:
                    - CIDR for the OpenShift Pods (immutable).
                type: str
            service_cidr:
                description:
                    - CIDR for OpenShift Services (immutable).
                type: str
            outbound_type:
                description:
                    - The OutboundType used for egress traffic.
                type: str
                choices:
                    - Loadbalancer
                    - UserDefinedRouting
            preconfigured_nsg:
                description:
                    - Specifies whether subnets are pre-attached with an NSG
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Disabled
    master_profile:
        description:
            - Configuration for OpenShift master VMs.
        type: dict
        suboptions:
            vm_size:
                description:
                    - Size of agent VMs (immutable).
                type: str
            subnet_id:
                description:
                    - The Azure resource ID of the master subnet (immutable).
                required: true
                type: str
            encryption_at_host:
                description:
                    - Whether master virtual machines are encrypted at host.
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Disabled
            disk_encryption_set_id:
                description:
                    - The resource ID of an associated DiskEncryptionSet, if applicable.
                type: str
    worker_profiles:
        description:
            - Configuration for OpenShift worker Vms.
        type: list
        elements: dict
        suboptions:
            name:
                description: name of the worker profile (immutable).
                type: str
                required: true
                choices:
                    - worker
            vm_size:
                description:
                    - The size of the worker Vms (immutable).
                type: str
            disk_size:
                description:
                    - The disk size of the worker VMs in GB. Must be 128 or greater (immutable).
                type: int
            subnet_id:
                description:
                    - The Azure resource ID of the worker subnet (immutable).
                type: str
                required: true
            count:
                description:
                    - The number of worker VMs. Must be between 3 and 20 (immutable).
                type: int
            encryption_at_host:
                description:
                    - Whether worker virtual machines are encrypted at host.
                type: str
                choices:
                    - Disabled
                    - Enabled
                default: Disabled
            disk_encryption_set_id:
                description:
                    - The resource ID of an associated DiskEncryptionSet, if applicable.
                type: str
    api_server_profile:
        description:
            - API server configuration.
        type: dict
        suboptions:
            visibility:
                description:
                    - API server visibility.
                type: str
                default: Public
                choices:
                    - Public
                    - Private
            ip:
                description:
                    - IP address of api server (immutable), only appears in response.
                type: str
            url:
                description:
                    - Url of api server (immutable), only appears in response.
                type: str
    ingress_profiles:
        description:
            - Ingress profiles configuration. only one profile is supported at the current API version.
        type: list
        elements: dict
        suboptions:
            visibility:
                description:
                    - Ingress visibility.
                type: str
                default: Public
                choices:
                    - Public
                    - Private
            name:
                description:
                    - Name of the ingress  (immutable).
                type: str
                default: default
                choices:
                    - default
            ip:
                description:
                    - IP of the ingress (immutable), only appears in response.
                type: str
    provisioning_state:
        description:
            - The current deployment or provisioning state, which only appears in the response.
        type: str
    state:
        description:
            - Assert the state of the OpenShiftManagedCluster.
            - Use C(present) to create or update an OpenShiftManagedCluster and C(absent) to delete it.
        default: present
        type: str
        choices:
            - absent
            - present
extends_documentation_fragment:
    - azure.azcollection.azure
    - azure.azcollection.azure_tags
author:
    - Haiyuan Zhang (@haiyuazhang)
'''

EXAMPLES = '''
- name: Create openshift cluster
  azure_rm_openshiftmanagedcluster:
    resource_group: "myResourceGroup"
    name: "myCluster"
    location: "eastus"
    cluster_profile:
      cluster_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/clusterResourceGroup"
      domain: "mydomain"
    service_principal_profile:
      client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      client_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    network_profile:
      pod_cidr: "10.128.0.0/14"
      service_cidr: "172.30.0.0/16"
    worker_profiles:
      - name: worker
        vm_size: "Standard_D4s_v3"
        subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/Microsoft.Network/virtualNetworks/myVnet/subnets/worker"
        disk_size: 128
        count: 3
    master_profile:
      vm_size: "Standard_D8s_v3"
      subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/master"
- name: Create openshift cluster with multi parameters
  azure_rm_openshiftmanagedcluster:
    resource_group: "myResourceGroup"
    name: "myCluster"
    location: "eastus"
    cluster_profile:
      cluster_resource_group_id: "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/clusterResourceGroup"
      domain: "mydomain"
      fips_validated_modules: Enabled
    service_principal_profile:
      client_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      client_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    network_profile:
      pod_cidr: "10.128.0.0/14"
      service_cidr: "172.30.0.0/16"
      outbound_type: Loadbalancer
      preconfigured_nsg: Disabled
    worker_profiles:
      - name: worker
        vm_size: "Standard_D4s_v3"
        subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/Microsoft.Network/virtualNetworks/myVnet/subnets/worker"
        disk_size: 128
        count: 3
        encryption_at_host: Disabled
    master_profile:
      vm_size: "Standard_D8s_v3"
      subnet_id: "/subscriptions/xx-xx-xx-xx-xx/resourceGroups/myResourceGroup/providers/Microsoft.Network/virtualNetworks/myVnet/subnets/master"
      encryption_at_host: Disabled
- name: Delete OpenShift Managed Cluster
  azure_rm_openshiftmanagedcluster:
    resource_group: myResourceGroup
    name: myCluster
    location: eastus
    state: absent
'''

RETURN = '''
id:
    description:
        - Resource ID.
    returned: always
    type: str
    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus/providers/Microsoft.RedHatOpenShift/openShiftClusters/mycluster
name:
    description:
        - Resource name.
    returned: always
    type: str
    sample: mycluster
type:
    description:
        - Resource type.
    returned: always
    type: str
    sample: Microsoft.RedHatOpenShift/openShiftClusters
location:
    description:
        - Resource location.
    returned: always
    type: str
    sample: eatus
properties:
    description:
        - Properties of a OpenShift managed cluster.
    returned: always
    type: complex
    sample: null
    contains:
        provisioningState:
            description:
                - The current deployment or provisioning state, which only appears in the response.
            returned: always
            type: str
            sample: Creating
        clusterProfile:
            description:
                - Configuration for Openshift cluster.
            returned: always
            type: complex
            contains:
                domain:
                    description:
                        - Domain for the cluster.
                    returned: always
                    type: str
                    sample: mycluster
                version:
                    description:
                        - Openshift version.
                    returned: always
                    type: str
                    sample: 4.4.17
                resourceGroupId:
                    description:
                        - The ID of the cluster resource group.
                    returned: always
                    type: str
                    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus-cluster
                fipsValidatedModules:
                    description:
                        - If FIPS validated crypto modules are used
                    type: str
                    returned: always
                    sample: Enabled
        servicePrincipalProfile:
            description:
                - Service principal.
            type: complex
            returned: always
            contains:
                clientId:
                    description: Client ID of the service principal.
                    returned: always
                    type: str
                    sample: xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx
        networkProfile:
            description:
                - Configuration for OpenShift networking.
            returned: always
            type: complex
            contains:
                podCidr:
                    description:
                        - CIDR for the OpenShift Pods.
                    returned: always
                    type: str
                    sample: 10.128.0.0/14
                serviceCidr:
                    description:
                        - CIDR for OpenShift Services.
                    type: str
                    returned: always
                    sample: 172.30.0.0/16
                outboundType:
                    description:
                        - The OutboundType used for egress traffic.
                    type: str
                    returned: always
                    sample: Loadbalancer
                preconfiguredNSG:
                    description:
                        - Specifies whether subnets are pre-attached with an NSG
                    type: str
                    returned: always
                    sample: Disabled
        masterProfile:
            description:
                - Configuration for OpenShift master VMs.
            returned: always
            type: complex
            contains:
                vmSize:
                    description:
                        - Size of agent VMs (immutable).
                    type: str
                    returned: always
                    sample: Standard_D8s_v3
                subnetId:
                    description:
                        - The Azure resource ID of the master subnet (immutable).
                    type: str
                    returned: always
                    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus/providers/Microsoft.Network/
                            virtualNetworks/mycluster-vnet/subnets/mycluster-worker
                encryptionAtHost:
                    description:
                        - Whether master virtual machines are encrypted at host.
                    type: str
                    returned: always
                    sample: Disabled
                disk_encryption_set_id:
                    description:
                        - The resource ID of an associated DiskEncryptionSet, if applicable.
                    type: str
                    returned: successd
                    sample: null
        workerProfiles:
            description:
                - Configuration of OpenShift cluster VMs.
            returned: always
            type: complex
            contains:
                name:
                    description:
                        - Unique name of the pool profile in the context of the subscription and resource group.
                    returned: always
                    type: str
                    sample: worker
                count:
                    description:
                        - Number of agents (VMs) to host docker containers.
                    returned: always
                    type: int
                    sample: 3
                vmSize:
                    description:
                        - Size of agent VMs.
                    returned: always
                    type: str
                    sample: Standard_D4s_v3
                diskSizeGB:
                    description:
                        - disk size in GB.
                    returned: always
                    type: int
                    sample: 128
                subnetId:
                    description:
                        - Subnet ID for worker pool.
                    returned: always
                    type: str
                    sample: /subscriptions/xx-xx-xx-xx/resourceGroups/mycluster-eastus/providers/Microsoft.Network/
                            virtualNetworks/mycluster-vnet/subnets/mycluster-worker
                encryptionAtHost:
                    description:
                        - Whether worker virtual machines are encrypted at host.
                    type: str
                    returned: always
                    sample: Disabled
        ingressProfiles:
            description:
                - Ingress configruation.
            returned: always
            type: list
            sample: [{"name": "default", "visibility": "Public"}, ]
        apiserverProfile:
            description:
                - API server configuration.
            returned: always
            type: complex
            contains:
                visibility:
                    description:
                        - api server visibility.
                    returned: always
                    type: str
                    sample: Public
'''

import time
import json
import random
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_ext import AzureRMModuleBaseExt
from ansible_collections.azure.azcollection.plugins.module_utils.azure_rm_common_rest import GenericRestClient

class Actions:
    NoAction, Create, Update, Delete = range(4)


class AzureRMOpenShiftManagedClusters(AzureRMModuleBaseExt):
    def __init__(self):
        self.module_arg_spec = dict(
            resource_group=dict(
                type='str',
                required=True
            ),
            name=dict(
                type='str',
                required=True
            ),
            location=dict(
                type='str',
                required=True
            ),
            cluster_profile=dict(
                type='dict',
                default=dict(),
                options=dict(
                    pull_secret=dict(
                        type='str',
                        no_log=True,
                    ),
                    cluster_resource_group_id=dict(
                        type='str',
                    ),
                    domain=dict(
                        type='str',
                    ),
                    version=dict(
                        type='str',
                    ),
                    fips_validated_modules=dict(
                        type='str',
                        choices=['Enabled', 'Disabled'],
                        default='Disabled'
                    ),
                ),
            ),
            identity=dict(
                type="dict",
                options=dict(
                    type=dict(
                        type='str',
                        choices=[
                            'None',
                            'SystemAssigned',
                            'UserAssigned',
                            'SystemAssigned,UserAssigned'
                        ]
                    ),
                    user_assigned_identities=dict(
                        type='dict'
                    )
                ),
            ),
            service_principal_profile=dict(
                type='dict',
                options=dict(
                    client_id=dict(
                        type='str',
                    ),
                    client_secret=dict(
                        type='str',
                        no_log=True,
                    )
                )
            ),
            network_profile=dict(
                type='dict',
                options=dict(
                    pod_cidr=dict(
                        type='str',
                        default='10.128.0.0/14',
                    ),
                    service_cidr=dict(
                        type='str',
                        default='172.30.0.0/16',
                    ),
                    outbound_type=dict(
                        type='str',
                        choices=['Loadbalancer', 'UserDefinedRouting']
                    ),
                    preconfigured_nsg=dict(
                        type='str',
                        choices=['Disabled', 'Enabled'],
                        default='Disabled'
                    ),
                    load_balancer_profile=dict(
                        type='dict',
                        options=dict(
                            managed_outbound_ips=dict(
                                type='dict',
                                options=dict(
                                    count=dict(
                                        type='int'
                                    )
                                )
                            )
                        )
                    )
                ),
                default=dict(
                    pod_cidr="10.128.0.0/14",
                    service_cidr="172.30.0.0/16"
                )
            ),
            platform_workload_identity_profile=dict(
              type='dict',
              options=dict(
                  upgradeable_to=dict(
                      type='str'
                  ),
                  platform_workload_identities=dict(
                      type='dict',
                  )
              )
            ),
            master_profile=dict(
                type='dict',
                options=dict(
                    vm_size=dict(
                        type='str'
                    ),
                    subnet_id=dict(
                        type='str',
                        required=True
                    ),
                    encryption_at_host=dict(
                        type='str',
                        choices=['Disabled', 'Enabled'],
                        default='Disabled'
                    ),
                    disk_encryption_set_id=dict(
                        type='str'
                    )
                )
            ),
            worker_profiles=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                        required=True,
                        choices=['worker']
                    ),
                    count=dict(
                        type='int',
                        default=3,
                    ),
                    vm_size=dict(
                        type='str'
                    ),
                    subnet_id=dict(
                        type='str',
                        required=True
                    ),
                    disk_size=dict(
                        type='int',
                    ),
                    encryption_at_host=dict(
                        type='str',
                        choices=['Disabled', 'Enabled'],
                        default='Disabled'
                    ),
                    disk_encryption_set_id=dict(
                        type='str'
                    )
                )
            ),
            api_server_profile=dict(
                type='dict',
                options=dict(
                    visibility=dict(
                        type='str',
                        choices=['Public', 'Private'],
                        default='Public'
                    ),
                    url=dict(
                        type='str',
                    ),
                    ip=dict(
                        type='str',
                    )
                )
            ),
            ingress_profiles=dict(
                type='list',
                elements='dict',
                options=dict(
                    name=dict(
                        type='str',
                        choices=['default'],
                        default='default'
                    ),
                    visibility=dict(
                        type='str',
                        choices=['Public', 'Private'],
                        default='Public'
                    ),
                    ip=dict(
                        type='str',
                    )
                )
            ),
            provisioning_state=dict(
                type='str',
            ),
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent']
            ),
            rp_mode=dict(
                type='str',
                choices=['production', 'development']
            ),
            api_version=dict(
                type='str',
                default='2023-11-22'
            )
        )

        self.resource_group = None
        self.name = None

        self.results = dict(changed=False)
        self.mgmt_client = None
        self.state = None
        self.url = None
        self.status_code = [200, 201, 202]
        self.to_do = Actions.NoAction

        self.body = {}
        self.body['properties'] = {}
        self.query_parameters = {}
        self.header_parameters = {}

        self.api_version = '2023-11-22'
        self.rp_mode = 'production'
        self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'

        super(AzureRMOpenShiftManagedClusters, self).__init__(derived_arg_spec=self.module_arg_spec,
                                                              supports_check_mode=True,
                                                              supports_tags=True)

    def exec_module(self, **kwargs):
        for key in list(self.module_arg_spec.keys()) + ['tags']:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            elif kwargs[key] is not None:
                if key == 'cluster_profile':
                    cluster_profile = dict()
                    pull_secret = kwargs[key].get("pull_secret")
                    if pull_secret:
                        cluster_profile["pullSecret"] = pull_secret
                    cluster_resourcegroup = kwargs[key].get("cluster_resource_group_id")
                    if cluster_resourcegroup:
                        cluster_profile["resourceGroupId"] = cluster_resourcegroup
                    domain = kwargs[key].get("domain")
                    if domain:
                        cluster_profile["domain"] = domain
                    version = kwargs[key].get("version")
                    if version:
                        cluster_profile["version"] = version
                    fips_validated_modules = kwargs[key].get("fips_validated_modules")
                    if fips_validated_modules:
                        cluster_profile["fipsValidatedModules"] = fips_validated_modules

                    if cluster_profile:
                        self.body['properties']['clusterProfile'] = cluster_profile
                elif key == 'service_principal_profile':
                    spp = dict()
                    client_id = kwargs[key].get('client_id')
                    if client_id:
                        spp["ClientId"] = client_id
                    client_secret = kwargs[key].get('client_secret')
                    if client_secret:
                        spp["clientSecret"] = client_secret

                    if spp:
                        self.body['properties']['servicePrincipalProfile'] = spp
                elif key == 'identity':
                    identity = dict()
                    type = kwargs[key].get('type')
                    if type:
                        identity['type'] = type
                    uaids = kwargs[key].get('user_assigned_identities')
                    if uaids:
                        identity['userAssignedIdentities'] = uaids
                    if identity:
                        self.body['identity'] = identity
                elif key == 'platform_workload_identity_profile':
                    pwip = dict()
                    upgradeable_to = kwargs[key].get('upgradeable_to')
                    if upgradeable_to:
                        pwip['upgradeableTo'] = upgradeable_to
                    pwids = dict()
                    workload_identities = kwargs[key].get('platform_workload_identities', dict())
                    if workload_identities:
                        for key, value in workload_identities.items():
                            pwids[key] = dict(resourceId=value.get('resource_id'))
                    if pwids:
                        pwip['platformWorkloadIdentities'] = pwids
                    if pwip:
                        self.body['properties']['platformWorkloadIdentityProfile'] = pwip
                elif key == 'network_profile':
                    network_profile = dict()
                    pod_cidr = kwargs[key].get("pod_cidr")
                    if pod_cidr:
                        network_profile["podCidr"] = pod_cidr
                    service_cidr = kwargs[key].get("service_cidr")
                    if service_cidr:
                        network_profile['serviceCidr'] = service_cidr
                    outbound_type = kwargs[key].get("outbound_type")
                    if outbound_type:
                        network_profile['outboundType'] = outbound_type
                    preconfigured_nsg = kwargs[key].get("preconfigured_nsg")
                    if preconfigured_nsg:
                        network_profile['preconfiguredNSG'] = preconfigured_nsg

                    load_balancer_profile = kwargs[key].get("load_balancer_profile")
                    if load_balancer_profile:
                        lbp = dict()
                        moips = dict()
                        managed_outbound_ips = load_balancer_profile.get("managed_outbound_ips")
                        if managed_outbound_ips:
                            managed_outbound_ip_count = managed_outbound_ips.get("count")
                            if managed_outbound_ip_count:
                                moips["count"] = managed_outbound_ip_count
                        if moips:
                            lbp["managedOutboundIps"] = moips
                        if lbp:
                            network_profile["loadBalancerProfile"] = lbp

                    if network_profile:
                        self.body['properties']['networkProfile'] = network_profile
                elif key == 'master_profile':
                    master_profile = {}
                    subnet_id = kwargs[key].get('subnet_id')
                    if subnet_id:
                        master_profile['subnetId'] = kwargs[key].get('subnet_id')
                    disk_encryption_set_id = kwargs[key].get('disk_encryption_set_id')
                    if disk_encryption_set_id:
                        master_profile['encryptionAtHost'] = disk_encryption_set_id
                    encryption_at_host = kwargs[key].get('encryption_at_host')
                    if encryption_at_host:
                        master_profile['encryptionAtHost'] = encryption_at_host
                    vm_size = kwargs[key].get('vm_size')
                    if vm_size:
                        master_profile['vmSize'] = vm_size

                    if master_profile:
                        self.body['properties']['masterProfile'] = master_profile
                elif key == 'worker_profiles':
                    worker_profiles = list()
                    for item in kwargs[key]:
                        worker_profile = {}
                        name = item.get('name')
                        if name:
                            worker_profile['name'] = name
                        subnet_id = item.get('subnet_id')
                        if subnet_id:
                            worker_profile['subnetId'] = subnet_id
                        count = item.get('count')
                        if count:
                            worker_profile['count'] = count
                        vm_size = item.get('vm_size')
                        if vm_size:
                            worker_profile['vmSize'] = item.get('vm_size')
                        disk_size = item.get('disk_size')
                        if disk_size:
                            worker_profile['diskSizeGB'] = disk_size
                        encryption_at_host = item.get('encryption_at_host')
                        if encryption_at_host:
                            worker_profile['encryptionAtHost'] = encryption_at_host
                        encryption_set = item.get('disk_encryption_set_id')
                        if encryption_set:
                            worker_profile['DiskEncryptionSetId'] = encryption_set

                        if worker_profile:
                            worker_profiles.append(worker_profile)
                    if worker_profiles:
                        self.body['properties']['workerProfiles'] = worker_profiles
                elif key == 'api_server_profile':
                    api_server_profile = dict()
                    visibility = kwargs[key].get("visibility")
                    if visibility:
                        api_server_profile["visibility"] = visibility
                    if api_server_profile:
                        self.body['properties']['apiserverProfile'] = api_server_profile
                elif key == 'ingress_profiles':
                    ingress_profiles = list()
                    for profile in kwargs[key]:
                        ip = dict()
                        name = profile.get("name")
                        if name:
                            ip["name"] = name
                        visibility = profile.get("visibility")
                        if visibility:
                            ip["visibility"] = visibility
                        if ip:
                            ingress_profiles.append(ip)
                    if ingress_profiles:
                        self.body['properties']['ingressProfiles'] = ingress_profiles
                # elif key == 'provisioning_state':
                #     self.body['properties']['provisioningState'] = kwargs[key]
                elif key == 'rp_mode':
                    self.rp_mode = kwargs[key]
                elif key == 'api_version':
                    self.api_version = kwargs[key]
                else:
                    self.body[key] = kwargs[key]

        response = None

        self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient,
                                                    base_url=self._cloud_environment.endpoints.resource_manager)
        self.query_parameters['api-version'] = self.api_version
        self.results["api_version"] = self.api_version
        if self.rp_mode != "production":
            self.results["rp_mode"] = self.rp_mode

        self.url = path.join('subscriptions',
                    self.subscription_id,
                    'resourceGroups',
                    self.resource_group,
                    'providers',
                    'Microsoft.RedHatOpenShift',
                    'openShiftClusters',
                    self.name)

        old_response = self.get_resource()

        if not old_response:
            self.log("OpenShiftManagedCluster instance doesn't exist")

            if self.state == 'absent':
                self.log("Old instance didn't exist")
            else:
                self.to_do = Actions.Create
        else:
            self.log('OpenShiftManagedCluster instance already exists')

            if self.state == 'absent':
                self.to_do = Actions.Delete
            else:
                modifiers = {}
                # self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
                # self.results['modifiers'] = modifiers
                # self.results['compare'] = []
                # if 'workProfiles' in self.body['properties']:
                #     self.body['properties'].pop('workerProfiles')
                # if not self.default_compare(modifiers, self.body, old_response, '', self.results):
                #     self.to_do = Actions.Update
                #self.fail("module doesn't support cluster update yet")
                self.results["id"] = old_response["id"]
                self.results["name"] = old_response["name"]
                self.results["type"] = old_response["type"]
                self.results["location"] = old_response["location"]
                self.results["properties"] = old_response["properties"]
                self.results["identity"] = old_response.get("identity")
                self.results["tags"] = old_response.get("tags")
                self.results["systemData"] = old_response.get("systemData")
                return self.results

        if (self.to_do == Actions.Create) or (self.to_do == Actions.Update):
            self.log('Need to Create / Update the OpenShiftManagedCluster instance')

            if self.check_mode:
                self.results['changed'] = True
                return self.results

            response = self.create_update_resource()

            self.results['changed'] = True
            self.log('Creation / Update done')
        elif self.to_do == Actions.Delete:
            self.log('OpenShiftManagedCluster instance deleted')
            self.results['changed'] = True

            if self.check_mode:
                return self.results

            self.delete_resource()

            # make sure instance is actually deleted, for some Azure resources, instance is hanging around
            # for some time after deletion -- this should be really fixed in Azure
            while self.get_resource():
                time.sleep(20)
        else:
            self.log('OpenShiftManagedCluster instance unchanged')
            self.results['changed'] = False
            response = old_response

        if response:
            self.results["id"] = response["id"]
            self.results["name"] = response["name"]
            self.results["type"] = response["type"]
            self.results["location"] = response["location"]
            self.results["properties"] = response["properties"]
            self.results["identity"] = response.get("identity")
            self.results["tags"] = response.get("tags")
            self.results["systemData"] = response.get("systemData")

        return self.results

    def create_update_resource(self):

        if self.to_do == Actions.Create:
            required_profile_for_creation = ["workerProfiles", "clusterProfile", "masterProfile"]

            if 'properties' not in self.body:
                self.fail('{0} are required for creating a openshift cluster'.format(
                    '[worker_profile, cluster_profile, service_principal_profile, master_profile]'))
            for profile in required_profile_for_creation:
                if profile not in self.body['properties']:
                    self.fail('{0} is required for creating a openshift cluster'.format(profile))
            if "servicePrincipalProfile" not in self.body['properties'] and \
               "platformWorkloadIdentityProfile" not in self.body['properties']:
                self.fail('Either service_principal_profile or platform_workload_identity_profile is required for creating an openshift cluster\n{0}'.format(
                    str(self.body)
                ))

            self.set_default()

        try:
            # RP_MODE=development hack
            if self.rp_mode == "development":
                self.mgmt_client._client._base_url = "https://localhost:8443/"
                self.mgmt_client._client._pipeline._transport.connection_config.verify = False

            response = self.mgmt_client.query(self.url,
                                              'PUT',
                                              self.query_parameters,
                                              self.header_parameters,
                                              self.body,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as exc:
            self.log('Error attempting to create the OpenShiftManagedCluster instance.')
            self.fail('Error creating the OpenShiftManagedCluster instance: {0}'
                '\n{1}\n{2}'.format(str(self.body), str(exc), str(self.results)))
        if hasattr(response, 'body'):
            response = json.loads(response.body())
        elif hasattr(response, 'context'):
            response = response.context['deserialized_data']
        else:
            self.fail("Create or Updating fail, no match message return, return info as {0}".format(response))

        return response

    def delete_resource(self):
        # self.log('Deleting the OpenShiftManagedCluster instance {0}'.format(self.))
        try:
            if self.rp_mode == "development":
                self.mgmt_client._client._base_url = "https://localhost:8443/"
                self.mgmt_client._client._pipeline._transport.connection_config.verify = False

            response = self.mgmt_client.query(self.url,
                                              'DELETE',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
        except Exception as e:
            self.log('Error attempting to delete the OpenShiftManagedCluster instance.')
            self.fail('Error deleting the OpenShiftManagedCluster instance: {0}'.format(str(e)))

        return True

    def get_resource(self):
        # self.log('Checking if the OpenShiftManagedCluster instance {0} is present'.format(self.))
        found = False
        try:
            if self.rp_mode == "development":
                self.mgmt_client._client._base_url = "https://localhost:8443/"
                self.mgmt_client._client._pipeline._transport.connection_config.verify = False

            response = self.mgmt_client.query(self.url,
                                              'GET',
                                              self.query_parameters,
                                              self.header_parameters,
                                              None,
                                              self.status_code,
                                              600,
                                              30)
            found = True
            response = json.loads(response.body())
            found = True
            self.log("Response : {0}".format(response))
            # self.log("OpenShiftManagedCluster instance : {0} found".format(response.name))
        except Exception as e:
            self.log('Did not find the OpenShiftManagedCluster instance.')
        if found is True:
            return response

        return False

#    def random_id(self):
#        import random
#        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(8))

# Added per Mangirdas Judeikis (RED HAT INC) to fix first letter of cluster domain beginning with digit ; currently not supported
    def random_id(self):
        random_id = (''.join(random.choice('abcdefghijklmnopqrstuvwxyz')) +
                     ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
                             for key in range(7)))
        return random_id
###

    def set_default(self):
        if 'apiserverProfile' not in self.body['properties']:
            api_profile = dict(visibility="Public")
            self.body['properties']['apiserverProfile'] = api_profile
        if 'ingressProfiles' not in self.body['properties']:
            ingress_profile = dict(visibility="Public", name="default")
            self.body['properties']['ingressProfiles'] = [ingress_profile]
        else:
            # hard code the ingress profile name as default, so user don't need to specify it
            for profile in self.body['properties']['ingressProfiles']:
                profile['name'] = "default"
        if 'name' not in self.body['properties']['workerProfiles'][0]:
            self.body['properties']['workerProfiles'][0]['name'] = 'worker'
        if 'vmSize' not in self.body['properties']['workerProfiles'][0]:
            self.body['properties']['workerProfiles'][0]['vmSize'] = "Standard_D4s_v3"
        if 'diskSizeGB' not in self.body['properties']['workerProfiles'][0]:
            self.body['properties']['workerProfiles'][0]['diskSizeGB'] = 128
        if 'vmSize' not in self.body['properties']['masterProfile']:
            self.body['properties']['masterProfile']['vmSize'] = "Standard_D8s_v3"
        if 'pullSecret' not in self.body['properties']['clusterProfile']:
            self.body['properties']['clusterProfile']['pullSecret'] = ''
        # if domain is not set in cluster profile or it is set to an empty string or null value then generate a random domain
        self.random_id = self.random_id()
        if 'domain' not in self.body['properties']['clusterProfile'] or not self.body['properties']['clusterProfile']['domain']:
            self.body['properties']['clusterProfile']['domain'] = self.random_id
        if 'resourceGroupId' not in self.body['properties']['clusterProfile'] or not self.body['properties']['clusterProfile']['resourceGroupId']:
            resourcegroup_id = "/subscriptions/" + self.subscription_id + "/resourceGroups/" + self.name + "-" + self.random_id
            self.body['properties']['clusterProfile']['resourceGroupId'] = resourcegroup_id


def main():
    AzureRMOpenShiftManagedClusters()


if __name__ == '__main__':
    main()
