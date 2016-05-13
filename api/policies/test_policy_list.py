# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tempest.lib import decorators

from senlin.tests.tempest.api import base
from senlin.tests.tempest.common import constants


class TestPolicyList(base.BaseSenlinTest):

    @classmethod
    def resource_setup(cls):
        super(TestPolicyList, cls).resource_setup()
        # Create policy
        params = {
            'policy': {
                'name': 'test-policy',
                'spec': constants.spec_scaling_policy
            }
        }
        cls.policy = cls.client.create_obj('policies', params)['body']

    @classmethod
    def resource_cleanup(cls):
        # Delete policy
        cls.client.delete_obj('policies', cls.policy['id'])
        super(TestPolicyList, cls).resource_cleanup()

    @decorators.idempotent_id('67ce5d15-c1fd-402f-bcd8-2974dbd93da8')
    def test_list_policy(self):
        res = self.client.list_objs('policies')

        # Verify resp of policy list API
        self.assertEqual(200, res['status'])
        self.assertIsNone(res['location'])
        self.assertIsNotNone(res['body'])
        policies = res['body']
        ids = []
        for policy in policies:
            for key in ['created_at', 'data', 'domain', 'id', 'name',
                        'project', 'spec', 'type', 'updated_at', 'user']:
                self.assertIn(key, policy)
            ids.append(policy['id'])
        self.assertIn(self.policy['id'], ids)
