# -*- coding: utf-8 -
#
# This file is part of restkit released under the MIT license. 
# See the NOTICE for more information.

"""
gevent connection manager. 
"""

from gevent.coros import RLock

from .base import Manager

class GeventManager(Manager):

    def get_lock(self):
        return RLock()
