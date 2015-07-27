#!/usr/bin/python
# Copyright (c) 2015 Mirantis Inc.
#
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

import random
import sys
import time

from oslo_log import log
from oslo_config import cfg
import oslo_messaging as messaging


opts = [
    cfg.StrOpt('server_id',
               help='A string uniquely identifying target instance.'),
]
CONF = cfg.CONF
CONF.register_cli_opts(opts)

log.register_options(CONF)


rnd = random.Random()
logger = None


class RpcClient(object):
    def __init__(self, transport):
        target = messaging.Target(topic='example_rpc', version='1.0',
                                  server=CONF.server_id)
        self._client = messaging.RPCClient(transport, target)

    def example_method(self, param1):
        logger.info('Calling example_method with param1=%s' % param1)
        res = self._client.prepare(timeout=240).call({}, 'example_method', param1=param1)
        logger.info('Server returned %s' % res)
        return res


def setup():
    global logger

    CONF(sys.argv[1:], project='example_rpc_server')

    log.setup(CONF, 'example_rpc_server')
    logger = log.getLogger(__name__)


def main():
    setup()

    transport = messaging.get_transport(cfg.CONF)
    client = RpcClient(transport)

    while True:
        sec = rnd.randint(30, 180)
        client.example_method(sec)
        logger.info('Sleeping for %s seconds' % sec)
        time.sleep(sec)
        logger.info('Finished sleeping')


if __name__ == '__main__':
    main()

