# -*- coding: utf-8 -*-
#
# This file is part of couchapp released under the Apache 2 license. 
# See the NOTICE for more information.

import logging
import os
import re
import signal
import sys
import time
import traceback

from .pathtools.path import absolute_path
from .watchdog.observers import Observer
from .watchdog.events import FileSystemEventHandler
from .watchdog.utils import has_attribute

from ..errors import AppError
from ..localdoc import document
from ..util import json, remove_comments

log = logging.getLogger(__name__)

DEFAULT_UPDATE_DELAY = 5 # update delay in seconds

class CouchappEventHandler(FileSystemEventHandler):

    def __init__(self, doc, dbs, update_delay=DEFAULT_UPDATE_DELAY, 
            noatomic=False):
        super(CouchappEventHandler, self).__init__()

        self.update_delay = update_delay
        self.doc = doc
        self.dbs = dbs
        self.noatomic = noatomic
        self.last_update = None

        ignorefile = os.path.join(doc.docdir, '.couchappignore')
        if os.path.exists(ignorefile):
            with open(ignorefile, 'r') as f:
                self.ignores = json.loads(remove_comments(f.read()))

    def check_ignore(self, item):
        for ign in self.ignores:
            match = re.match(ign, item)
            if match:
                return True
        return False

    def maybe_update(self):
        if not self.last_update:
            return

        diff = time.time() - self.last_update
        if diff >= self.update_delay:
            self.doc.push(self.dbs, noatomic=self.noatomic, 
                    noindex=True)
            self.last_update = None

    def dispatch(self, ev):
        log.info("got change")
        if self.check_ignore(ev.src_path):
            return

        self.last_update = time.time()
        self.maybe_update()

class CouchappWatcher(object):

    SIG_QUEUE = []
    SIGNALS = map(
            lambda x: getattr(signal, "SIG%s" % x),
            "QUIT INT TERM".split())

    SIG_NAMES = dict(
            (getattr(signal, name), name[3:].lower()) \
                    for name in dir(signal) \
                    if name[:3] == "SIG" and name[3] != "_")

    def __init__(self, doc, dbs, update_delay=DEFAULT_UPDATE_DELAY, 
            noatomic=False):
        self.doc_path = absolute_path(doc.docdir)
        self.event_handler = CouchappEventHandler(doc, dbs,
                update_delay=update_delay, noatomic=noatomic)
        self.observer = Observer()
        self.observer.schedule(self.event_handler,
                self.doc_path, recursive=True)

    def init_signals(self):
        """\
        Initialize master signal handling. Most of the signals
        are queued. Child signals only wake up the master.
        """
        map(lambda s: signal.signal(s, self.signal), self.SIGNALS)
        signal.signal(signal.SIGCHLD, self.handle_chld)

    def signal(self, sig, frame):
        if len(self.SIG_QUEUE) < 5:
            self.SIG_QUEUE.append(sig)
        else:
            log.warn("Dropping signal: %s" % sig)

    def handle_chld(self, sig, frame):
        return

    def handle_quit(self):
        raise StopIteration

    def handle_int(self):
        raise StopIteration

    def handle_term(self):
        raise StopIteration

    def run(self):
        log.info("Starting to listen changes in '%s'", self.doc_path)
        self.init_signals()
        self.observer.start()
        while True:
            try:
                sig = self.SIG_QUEUE.pop(0) if len(self.SIG_QUEUE) else None
                if sig is None:
                    self.event_handler.maybe_update() 
                elif sig in self.SIG_NAMES:
                    signame = self.SIG_NAMES.get(sig)
                    handler = getattr(self, "handle_%s" % signame, None)
                    if not handler:
                        log.error("Unhandled signal: %s" % signame)
                        continue
                    log.info("handling signal: %s" % signame)
                    handler()
                else:
                    log.info("Ignoring unknown signal: %s" % sig)
                time.sleep(1)
            except StopIteration:
                self.halt()
            except KeyboardInterrupt:
                self.halt()
            except Exception, e:
                log.info("unhandled exception in main loop:\n%s" %
                        traceback.format_exc())
                sys.exit(-1)
        self.observer.join()

    def halt(self):
        self.observer.stop()
        sys.exit(0)                

def autopush(conf, path, *args, **opts):
    doc_path = None
    dest = None
    if len(args) < 2:
        doc_path = path
        if args:
            dest = args[0]
    else:
        doc_path = os.path.normpath(os.path.join(os.getcwd(), 
            args[0]))
        dest = args[1]

    if doc_path is None:
        raise AppError("You aren't in a couchapp.")

    conf.update(doc_path)
    doc = document(doc_path, create=False, 
            docid=opts.get('docid'))
    dbs = conf.get_dbs(dest)

    update_delay = opts.get('update_delay', DEFAULT_UPDATE_DELAY)
    noatomic = opts.get('no_atomic', False)

    watcher = CouchappWatcher(doc, dbs, update_delay=update_delay,
            noatomic=onoatomic)
    watcher.run()
