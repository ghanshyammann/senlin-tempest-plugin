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
from senlin.tests.tempest.api import utils


class TestActionList(base.BaseSenlinTest):

    @classmethod
    def resource_setup(cls):
        super(TestActionList, cls).resource_setup()
        cls.profile = utils.create_a_profile(cls)
        cls.cluster = utils.create_a_cluster(cls, cls.profile['id'])

    @classmethod
    def resource_cleanup(cls):
        # Delete cluster
        cls.delete_test_cluster(cls.cluster['id'])
        # Delete profile
        cls.delete_profile(cls.profile['id'])
        super(TestActionList, cls).resource_cleanup()

    @decorators.idempotent_id('2e47639b-7f58-4fb4-a147-a8c6bf184e97')
    def test_action_list(self):
        res = self.client.list_objs('actions')

        self.assertEqual(200, res['status'])
        self.assertIsNone(res['location'])
        self.assertIsNotNone(res['body'])

        actions = res['body']
        for action in actions:
            for key in ['action', 'cause', 'created_at', 'data',
                        'depended_by', 'depends_on', 'end_time', 'id',
                        'inputs', 'interval', 'name', 'outputs', 'owner',
                        'start_time', 'status', 'status_reason', 'target',
                        'timeout', 'updated_at']:
                self.assertIn(key, action)
