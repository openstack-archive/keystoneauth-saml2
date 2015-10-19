# -*- coding: utf-8 -*-

# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
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

import os
import uuid

from keystoneauth1 import loading
from keystoneauth1 import session
from lxml import etree
from oslo_config import fixture as config
from oslotest import base
from requests_mock.contrib import fixture as requests_mock

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
XMLDIR = os.path.join(ROOTDIR, 'examples', 'xml/')


def make_oneline(s):
    return etree.tostring(etree.XML(s)).replace(b'\n', b'')


def load_xml(filename):
    with open(XMLDIR + filename, 'rb') as f:
        return make_oneline(f.read())


class TestCase(base.BaseTestCase):

    """Test case base class for all unit tests."""

    TEST_ROOT_URL = 'http://127.0.0.1:5000/'
    TEST_URL = '%s%s' % (TEST_ROOT_URL, 'v3')

    TEST_USER = uuid.uuid4().hex
    TEST_USER_ID = uuid.uuid4().hex

    def setUp(self):
        super(TestCase, self).setUp()
        self.conf_fixture = self.useFixture(config.Config())

        self.requests = self.useFixture(requests_mock.Fixture())
        self.session = session.Session()

    def register_conf_options(self, group=None, section=None):
        loading.register_auth_conf_options(self.conf_fixture.conf, group=group)

        if section:
            self.conf_fixture.config(group=group, auth_section=section)
            loading.register_auth_conf_options(self.conf_fixture.conf,
                                               group=group)

        return self.conf_fixture
