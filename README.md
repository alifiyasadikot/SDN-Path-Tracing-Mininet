📘 SDN Path Tracing Tool using Mininet
🔹 Problem Statement

This project implements an SDN-based solution to identify and display the path taken by packets using Mininet and a POX controller.

🔹 Tools Used
Mininet
POX Controller
OpenFlow
🔹 Topology
2 Hosts (h1, h2)
1 Switch (s1)
🔹 How It Works
Controller handles packet_in events
Learns MAC addresses
Installs flow rules dynamically
Displays packet path from source to destination
🔹 Execution Steps
sudo mn --controller=remote
pingall
🔹 Output
Packet trace displayed
Flow rules installed
Successful communication (0% packet loss)
🔹 Proof of Execution

(Add your screenshots here)

🔹 Conclusion

This project demonstrates SDN concepts like centralized control, dynamic flow installation, and packet path tracing.
