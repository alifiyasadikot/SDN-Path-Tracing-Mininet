rom pox.core import core

log = core.getLogger()
paths = {}

def _handle_PacketIn(event):
    packet = event.parsed

    if not packet.parsed:
        return

    # Ignore multicast / noise
    if packet.dst.is_multicast:
        return

    dpid = event.connection.dpid
    src = str(packet.src)
    dst = str(packet.dst)

    if src not in paths:
        paths[src] = []

    if dpid not in paths[src]:
        paths[src].append(dpid)

    log.info(f"s{dpid}: {src} -> {dst}")

    # Print path when destination seen
    if src in paths and len(paths[src]) > 1:
        path = " -> ".join([f"s{x}" for x in paths[src]])

log.info(f"🔥 PATH: {src} -> {path} -> {dst}")

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Path Tracer (Safe Mode) Loaded")
