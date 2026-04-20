SDN PATH TRACING TOOL USING MININET

Problem Statement
This project implements an SDN-based system using Mininet and POX controller to identify and display the path taken by packets while demonstrating controller-switch interaction and flow rule behavior.

Objective

Track packet flow in the network
Display the forwarding path
Understand controller–switch interaction
Validate network using ping tests

Tools Used

Mininet
POX Controller
OpenFlow Protocol

Topology

2 Hosts → h1, h2
1 Switch → s1

Working Explanation
When a packet arrives at the switch and the destination is unknown, the switch sends a packet_in message to the controller. The controller learns the source MAC address and maps it to a port. If the destination is known, it installs a flow rule using match-action logic and forwards the packet. Future packets are forwarded directly by the switch without contacting the controller.

Additionally, the controller is modified to display the path taken by packets, allowing us to trace how packets travel through the network.

Execution Steps

Terminal 1 (Controller):
cd ~/pox
./pox.py forwarding.l2_learning

Terminal 2 (Mininet):
sudo mn -c
sudo mn --controller=remote
pingall

Output and Proof of Execution

Ping Test (Functional Validation):
[Add screenshot here: screenshots/output1.png]

Shows successful communication between hosts
0% packet loss confirms correct network behavior

Packet Trace Output:
[Add screenshot here: screenshots/output2.png]

Displays path taken by packet
Example: Host(h1) → s1 (port 2) → Host(h2)
Confirms correct forwarding path

Flow Rule and MAC Table:
[Add screenshot here: screenshots/output3.png]

Shows flow installation
Displays MAC-to-port mapping
Demonstrates controller decision-making

Code Modification
The _handle_PacketIn function in the POX controller is modified to:

Display packet path
Print MAC table
Improve visibility of network behavior

Example:
print("=== Packet Trace ===")
print(f"Host({packet.src}) -> s1 (port {in_port}) -> Host({packet.dst})")
print(f"MAC Table: {self.macToPort}")

Results

Packet path successfully displayed
Flow rules installed dynamically
Network communication successful (0% packet loss)

Conclusion
This project demonstrates key SDN concepts such as centralized control, dynamic flow rule installation, and packet path tracing. The implementation shows how a controller manages network behavior efficiently while providing visibility into packet flow.

Files Included

l2_learning.py → Modified controller code
commands.txt → Execution steps
screenshots folder → Proof of execution
