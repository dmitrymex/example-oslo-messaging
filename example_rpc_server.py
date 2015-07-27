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
               help='A string uniquely identifying current instance. Used'
                    'by server to distinguish instances.'),
]
CONF = cfg.CONF
CONF.register_cli_opts(opts)

log.register_options(CONF)


rnd = random.Random()
logger = None


class RpcEndpoint(object):
    def example_method(self, ctxt, param1):
        logger.info('Somebody is calling example_method with param1=%s'
                    % param1)

        sec = rnd.randint(30, 180)
        logger.info('Sleeping for %s seconds' % sec)
        time.sleep(sec)

        logger.info('Finished sleeping, returning result')
        return param1 * 4


def setup():
    global logger

    CONF(sys.argv[1:], project='example_rpc_server')

    log.setup(CONF, 'example_rpc_server')
    logger = log.getLogger(__name__)


def main():
    setup()

    logger.info('Running example_rpc_server from main()')

    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic='example_rpc', version='1.0',
                              server=CONF.server_id)
    server = messaging.get_rpc_server(transport, target,
                                      endpoints=[RpcEndpoint()])

    server.start()
    server.wait()


if __name__ == '__main__':
    main()
