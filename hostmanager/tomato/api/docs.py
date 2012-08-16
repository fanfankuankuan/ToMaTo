# -*- coding: utf-8 -*-
# ToMaTo (Topology management software) 
# Copyright (C) 2010 Dennis Schwerdel, University of Kaiserslautern
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from tomato import elements, connections

def DOC_ELEMENT_KVMQM():
    return elements.kvmqm.DOC
DOC_ELEMENT_KVMQM.__doc__ = elements.kvmqm.DOC

def DOC_ELEMENT_KVMQM_INTERFACE():
    return elements.kvmqm.DOC_IFACE
DOC_ELEMENT_KVMQM_INTERFACE.__doc__ = elements.kvmqm.DOC_IFACE


def DOC_ELEMENT_OPENVZ():
    return elements.openvz.DOC
DOC_ELEMENT_OPENVZ.__doc__ = elements.openvz.DOC

def DOC_ELEMENT_OPENVZ_INTERFACE():
    return elements.openvz.DOC_IFACE
DOC_ELEMENT_OPENVZ_INTERFACE.__doc__ = elements.openvz.DOC_IFACE


def DOC_ELEMENT_EXTERNAL_NETWORK():
    return elements.external_network.DOC
DOC_ELEMENT_EXTERNAL_NETWORK.__doc__ = elements.external_network.DOC


def DOC_ELEMENT_UDP_TUNNEL():
    return elements.udp_tunnel.DOC
DOC_ELEMENT_UDP_TUNNEL.__doc__ = elements.udp_tunnel.DOC


def DOC_ELEMENT_TINC():
    return elements.tinc.DOC
DOC_ELEMENT_TINC.__doc__ = elements.tinc.DOC


def DOC_CONNECTION_BRIDGE():
    return connections.bridge.DOC
DOC_CONNECTION_BRIDGE.__doc__ = connections.bridge.DOC

def DOC_CONNECTION_FIXED_BRIDGE():
    return connections.fixed_bridge.DOC
DOC_CONNECTION_FIXED_BRIDGE.__doc__ = connections.fixed_bridge.DOC