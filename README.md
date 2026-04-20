# SDN Path Tracing using Mininet and POX

## 📌 Problem Statement
The objective of this project is to implement an SDN-based solution that identifies and displays the path taken by packets across a network using Mininet and a POX controller.

---

## 🛠️ Tools & Technologies
- Mininet (Network Emulator)
- POX Controller (SDN Controller)
- OpenFlow Protocol
- Ubuntu (Linux)

---

## 🧠 Project Description
This project simulates a network topology using Mininet and connects it to a POX SDN controller. The controller performs the following:

- Learns MAC-to-port mappings (Learning Switch)
- Handles packet_in events
- Installs flow rules (match-action)
- Tracks switches traversed by packets
- Displays the full path from source to destination

---

## 🌐 Topology Used
Linear topology with 4 switches and 4 hosts:

h1 — s1 — s2 — s3 — s4 — h4

---

## ▶️ How to Run

### Step 1: Start Controller
```bash
cd ~/pox
./pox.py forwarding.l2_learning misc.path_tracer
Step 2: Start Mininet
sudo mn --controller=remote --topo linear,4
Step 3: Test Connectivity
pingall
h1 ping h4
✅ Expected Output
All hosts successfully ping each other (0% packet loss)
Controller logs show packet flow across switches

Example:

s1 → s2 → s3 → s4
PATH: h1 → s1 → s2 → s3 → s4 → h4
🧪 Test Cases
✔ Test Case 1: Normal Communication
pingall
Result: 0% packet loss
✔ Test Case 2: End-to-End Communication
h1 ping h4
Result: Successful packet delivery
⚠️ Note

Some DNS-related warnings may appear due to POX compatibility with Python 3.12. These do not affect the functionality of the project.

📸 Proof of Execution
Ping results (0% packet loss)
Path tracing logs
Running topology screenshots
🎯 Conclusion

The project successfully demonstrates SDN-based packet path tracing using Mininet and POX, fulfilling all requirements including controller logic, flow rule installation, and network behavior observation.
