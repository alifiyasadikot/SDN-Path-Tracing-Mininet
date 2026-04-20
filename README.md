📘 SDN Path Tracing Tool using Mininet
🎯 Objective

To implement an SDN-based system that identifies and displays the path taken by packets using Mininet and a POX controller.

🛠️ Tools Used
Mininet
POX Controller
OpenFlow
🌐 Topology
Hosts: h1, h2
Switch: s1
⚙️ Working

When a packet reaches the switch and the destination is unknown, the switch sends it to the controller (packet_in).
The controller learns MAC addresses and installs flow rules.

After that:

Packets are forwarded directly by the switch
Controller is not involved again

Additionally, packet tracing is implemented to display the path taken by packets.

💻 Execution Steps

Terminal 1:
cd ~/pox
./pox.py forwarding.l2_learning

Terminal 2:
sudo mn -c
sudo mn --controller=remote
pingall

📊 Output

📁 screenshots/output1.png

Ping test (0% packet loss)

📁 screenshots/output2.png

Packet trace showing path

📁 screenshots/output3.png

Flow rule and MAC table
🔧 Code Change

Modified _handle_PacketIn to:

Print packet path
Display MAC table

Example:

print("=== Packet Trace ===")
print(f"Host({packet.src}) -> s1 (port {event.port}) -> Host({packet.dst})")
✅ Result
Packet path displayed
Flow rules installed
Network working correctly
📌 Conclusion

This project demonstrates SDN concepts like centralized control, flow rule installation, and packet path tracing.
