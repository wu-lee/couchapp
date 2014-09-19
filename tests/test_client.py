# -*- coding: utf-8 -*-
#
# Copyright 2008,2009 Benoit Chesneau <benoitc@e-engura.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at#
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest2 as unittest
import tempfile
import os
from shutil import rmtree

from couchapp import client
import json


class ClientTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUuids(self):
        uuids = client.Uuids('http://localhost:5984')
        uuid = uuids.next()
        assert len(uuid) == 32
        del uuids
        # Test with trailing slash
        uuids = client.Uuids('http://localhost:5984/')
        uuid = uuids.next()
        assert len(uuid) == 32

if __name__ == '__main__':
    unittest.main()
