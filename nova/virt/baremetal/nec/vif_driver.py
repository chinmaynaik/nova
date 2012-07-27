# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2012 NTT DOCOMO, INC.
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

from webob import exc

from nova import exception
from nova import flags
from nova.openstack.common import log as logging

from nova.virt.baremetal.nec.vifinfo_client import VIFINFOClient
from nova.virt.baremetal import vif_driver

FLAGS = flags.FLAGS

LOG = logging.getLogger(__name__)


class NECVIFDriver(vif_driver.BareMetalVIFDriver):

    def _after_plug(self, instance, network, mapping, pif):
        client = VIFINFOClient(FLAGS.quantum_connection_host,
                               FLAGS.quantum_connection_port)
        client.create_vifinfo(mapping['vif_uuid'],
                              pif['datapath_id'],
                              pif['port_no'])

    def _after_unplug(self, instance, network, mapping, pif):
        client = VIFINFOClient(FLAGS.quantum_connection_host,
                               FLAGS.quantum_connection_port)
        try:
            client.delete_vifinfo(mapping['vif_uuid'])
        except (exception.NovaException,
                exc.HTTPNotFound, exc.HTTPInternalServerError), e:
            LOG.warn("client.delete_vifinfo(%s) is failed. (ignored): %s",
                     mapping['vif_uuid'], e)
