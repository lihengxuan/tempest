# Copyright 2013 NEC Corporation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import datetime

from tempest.api.compute import base
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc


class TenantUsagesNegativeTestJSON(base.BaseV2ComputeAdminTest):
    """Negative tests of compute tenant usages API"""

    @classmethod
    def setup_clients(cls):
        super(TenantUsagesNegativeTestJSON, cls).setup_clients()
        cls.adm_client = cls.os_admin.tenant_usages_client
        cls.client = cls.os_primary.tenant_usages_client

    @classmethod
    def resource_setup(cls):
        super(TenantUsagesNegativeTestJSON, cls).resource_setup()
        now = datetime.datetime.now()
        cls.start = cls._parse_strtime(now - datetime.timedelta(days=1))
        cls.end = cls._parse_strtime(now + datetime.timedelta(days=1))

    @classmethod
    def _parse_strtime(cls, at):
        # Returns formatted datetime
        return at.strftime('%Y-%m-%dT%H:%M:%S.%f')

    @decorators.attr(type=['negative'])
    @decorators.idempotent_id('8b21e135-d94b-4991-b6e9-87059609c8ed')
    def test_get_usage_tenant_with_empty_tenant_id(self):
        """Test getting tenant usage with empty tenant id should fail"""
        params = {'start': self.start,
                  'end': self.end}
        self.assertRaises(lib_exc.NotFound,
                          self.adm_client.show_tenant_usage,
                          '', **params)

    @decorators.attr(type=['negative'])
    @decorators.idempotent_id('4079dd2a-9e8d-479f-869d-6fa985ce45b6')
    def test_get_usage_tenant_with_invalid_date(self):
        """Test getting tenant usage with invalid time range should fail"""
        params = {'start': self.end,
                  'end': self.start}
        self.assertRaises(lib_exc.BadRequest,
                          self.adm_client.show_tenant_usage,
                          self.client.tenant_id, **params)

    @decorators.attr(type=['negative'])
    @decorators.idempotent_id('bbe6fe2c-15d8-404c-a0a2-44fad0ad5cc7')
    def test_list_usage_all_tenants_with_non_admin_user(self):
        """Test listing usage of all tenants by non-admin user is forbidden"""
        params = {'start': self.start,
                  'end': self.end,
                  'detailed': "1"}
        self.assertRaises(lib_exc.Forbidden,
                          self.client.list_tenant_usages, **params)
