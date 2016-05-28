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


class TestReceiverShow(base.BaseSenlinTest):

    @classmethod
    def resource_setup(cls):
        super(TestReceiverShow, cls).resource_setup()
        cls.profile = utils.create_a_profile(cls)
        cls.cluster = utils.create_a_cluster(cls, cls.profile['id'])
        # Create receiver
        cls.receiver = cls.create_receiver(cls.cluster['id'],
                                           'CLUSTER_RESIZE', 'webhook')

    @classmethod
    def resource_cleanup(cls):
        # Delete receiver
        cls.client.delete_obj('receivers', cls.receiver['id'])
        # Delete test cluster
        cls.delete_test_cluster(cls.cluster['id'])
        # Delete profile
        cls.delete_profile(cls.profile['id'])
        super(TestReceiverShow, cls).resource_cleanup()

    @decorators.idempotent_id('6a86b2e4-127a-4acc-b0ec-6f951b240e5b')
    def test_show_receiver(self):
        res = self.client.get_obj('receivers', self.receiver['id'])

        self.assertEqual(200, res['status'])
        self.assertIsNone(res['location'])
        self.assertIsNotNone(res['body'])
        receiver = res['body']
        for key in ['action', 'actor', 'channel', 'cluster_id',
                    'created_at', 'domain', 'id', 'name', 'params',
                    'project', 'type', 'updated_at', 'user']:
            self.assertIn(key, receiver)
