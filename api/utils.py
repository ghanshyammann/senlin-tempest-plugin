# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tempest.lib.common.utils import data_utils
from tempest.lib import exceptions

from senlin.tests.tempest.common import constants


def create_a_profile(cls, spec=None, name=None, metadata=None):
    """Utility function that generates a Senlin profile."""

    if spec is None:
        spec = constants.spec_nova_server

    if name is None:
        name = data_utils.rand_name("tempest-created-profile")

    params = {
        'profile': {
            'name': name,
            'spec': spec,
            'metadata': metadata,
        }
    }
    res = cls.client.create_obj('profiles', params)
    return res['body']['id']


def create_a_cluster(cls, profile_id, desired_capacity=0, min_size=0,
                     max_size=-1, timeout=None, metadata=None, name=None,
                     wait_timeout=None):
    """Utility function that generates a Senlin cluster.

    Create a cluster and return it after it is ACTIVE. The function is used for
    deduplicate code in API tests where an 'existing' cluster is needed.
    """
    if name is None:
        name = data_utils.rand_name("tempest-created-cluster")
    params = {
        'cluster': {
            'profile_id': profile_id,
            'desired_capacity': desired_capacity,
            'min_size': min_size,
            'max_size': max_size,
            'timeout': timeout,
            'metadata': metadata,
            'name': name
        }
    }
    res = cls.client.create_obj('clusters', params)
    cluster_id = res['body']['id']
    action_id = res['location'].split('/actions/')[1]
    cls.wait_for_status('actions', action_id, 'SUCCEEDED', wait_timeout)

    return cluster_id


def create_a_receiver(client, cluster_id, action, r_type=None, name=None,
                      params=None):
    """Utility function that generates a Senlin receiver."""

    if name is None:
        name = data_utils.rand_name("tempest-created-receiver")

    body = {
        'receiver': {
            'name': name,
            'cluster_id': cluster_id,
            'type': r_type or 'webhook',
            'action': action,
            'params': params or {}
        }
    }
    res = client.create_obj('receivers', body)
    return res['body']['id']


def delete_a_cluster(cls, cluster_id, wait_timeout=None):
    """Utility function that deletes a Senlin cluster."""
    res = cls.client.delete_obj('clusters', cluster_id)
    action_id = res['location'].split('/actions/')[1]
    cls.wait_for_status('actions', action_id, 'SUCCEEDED', wait_timeout)


def delete_a_profile(cls, profile_id, ignore_missing=False):
    """Utility function that deletes a Senlin profile."""
    res = cls.client.delete_obj('profiles', profile_id)
    if res['status'] == 404:
        if ignore_missing:
            return
        raise exceptions.NotFound()


def delete_a_receiver(client, receiver_id, ignore_missing=False):
    """Utility function that deletes a Senlin receiver."""
    res = client.delete_obj('receivers', receiver_id)
    if res['status'] == 404:
        if ignore_missing:
            return
        raise exceptions.NotFound()
