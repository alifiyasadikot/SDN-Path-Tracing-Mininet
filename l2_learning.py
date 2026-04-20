# Copyright 2011-2012 James McCauley
# Licensed under the Apache License, Version 2.0

"""
An L2 learning switch with SDN Path Tracing.

Modified to trace packet paths across multiple switches
in the topology: h1/h2 -- s1 -- s2 -- s3 -- h3/h4
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
import time

log = core.getLogger()

_flood_delay = 0

# Map MAC suffix to host name
def mac_to_host(mac_str):
    suffix_map = {
        "01": "h1", "02": "h2", "03": "h3", "04": "h4"
    }
    suffix = mac_str.split(":")[-1].lstrip("0") or "0"
    return suffix_map.get(suffix.zfill(2), mac_str)

# Map datapath ID to switch name
def dpid_to_switch(dpid):
    switch_map = {1: "s1", 2: "s2", 3: "s3"}
    return switch_map.get(dpid, f"s{dpid}")

# Topology: which switches connect to which
# s1(1) -- s2(2) -- s3(3)
TOPOLOGY = {
    1: [2],
    2: [1, 3],
    3: [2],
}

def find_path(src_dpid, dst_dpid):
    """BFS to find switch-level path between two switches."""
    if src_dpid == dst_dpid:
        return [src_dpid]
    visited = set()
    queue = [[src_dpid]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == dst_dpid:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in TOPOLOGY.get(node, []):
                queue.append(path + [neighbor])
    return None

# Track which switch each host was last seen on
host_location = {}  # mac -> dpid


class LearningSwitch(object):
    def __init__(self, connection, transparent):
        self.connection = connection
        self.transparent = transparent
        self.macToPort = {}
        connection.addListeners(self)
        self.hold_down_expired = _flood_delay == 0

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return
        if packet.dst.is_multicast and packet.type != packet.ARP_TYPE:
            return

        src_mac = str(packet.src)
        dst_mac = str(packet.dst)
        in_port = event.port
        this_dpid = event.dpid
        switch_name = dpid_to_switch(this_dpid)

        src_host = mac_to_host(src_mac)
        dst_host = mac_to_host(dst_mac)

        # Record where this host is
        host_location[src_mac] = this_dpid

        print("\n=== Packet Trace ===")
        print(f"  Packet-In at {switch_name} (port {in_port})")
        print(f"  Source : {src_host} ({src_mac})")
        print(f"  Dest   : {dst_host} ({dst_mac})")

        # If we know both endpoints, compute and show the full path
        if dst_mac in host_location:
            src_dpid = host_location[src_mac]
            dst_dpid = host_location[dst_mac]
            path_dpids = find_path(src_dpid, dst_dpid)
            if path_dpids:
                switches = " → ".join(dpid_to_switch(d) for d in path_dpids)
                full_path = f"{src_host} → {switches} → {dst_host}"
                print(f"  Path   : {full_path}")
        else:
            print(f"  Path   : {src_host} → {switch_name} → (dest location unknown yet)")

        print("====================\n")

        print(f"  MAC Table on {switch_name}: {self.macToPort}")

        def flood(message=None):
            msg = of.ofp_packet_out()
            if time.time() - self.connection.connect_time >= _flood_delay:
                if self.hold_down_expired is False:
                    self.hold_down_expired = True
                    log.info("%s: Flood hold-down expired -- flooding",
                             dpid_to_str(event.dpid))
                if message is not None:
                    log.debug(message)
                msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)

        def drop(duration=None):
            if duration is not None:
                if not isinstance(duration, tuple):
                    duration = (duration, duration)
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = duration[0]
                msg.hard_timeout = duration[1]
                msg.buffer_id = event.ofp.buffer_id
                self.connection.send(msg)
            elif event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                self.connection.send(msg)

        self.macToPort[packet.src] = event.port

        if not self.transparent:
            if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
                drop()
                return

        if packet.dst.is_multicast:
            flood()
        else:
            if packet.dst not in self.macToPort:
                flood("Port for %s unknown -- flooding" % (packet.dst,))
            else:
                port = self.macToPort[packet.dst]
                if port == event.port:
                    log.warning("Same port for packet from %s -> %s on %s.%s. Drop."
                                % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
                    drop(10)
                    return
                log.debug("installing flow for %s.%i -> %s.%i" %
                          (packet.src, event.port, packet.dst, port))
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = 10
                msg.hard_timeout = 30
                msg.actions.append(of.ofp_action_output(port=port))
                print(f"  Installing flow on {switch_name}: {src_host} → {dst_host} (out_port={port})")
                msg.data = event.ofp
                self.connection.send(msg)


class l2_learning(object):
    def __init__(self, transparent, ignore=None):
        core.openflow.addListeners(self)
        self.transparent = transparent
        self.ignore = set(ignore) if ignore else ()

    def _handle_ConnectionUp(self, event):
        if event.dpid in self.ignore:
            log.debug("Ignoring connection %s" % (event.connection,))
            return
        log.debug("Connection %s" % (event.connection,))
        LearningSwitch(event.connection, self.transparent)


def launch(transparent=False, hold_down=_flood_delay, ignore=None):
    try:
        global _flood_delay
        _flood_delay = int(str(hold_down), 10)
        assert _flood_delay >= 0
    except:
        raise RuntimeError("Expected hold-down to be a number")

    if ignore:
        ignore = ignore.replace(',', ' ').split()
        ignore = set(str_to_dpid(dpid) for dpid in ignore)

    core.registerNew(l2_learning, str_to_bool(transparent), ignore)
