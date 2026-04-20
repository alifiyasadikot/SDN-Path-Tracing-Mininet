# 🚀 SDN Path Tracing using Mininet and POX

---

## 📌 Problem Statement
The objective of this project is to implement an SDN-based solution that identifies and displays the path taken by packets across a network using Mininet and a POX controller.

---

## 🛠️ Tools & Technologies
- Mininet (Network Emulator)
- POX Controller (SDN Controller)
- OpenFlow Protocol
- Ubuntu Linux

---

## 🧠 Project Description
This project simulates a network using Mininet and connects it to a POX SDN controller.

The controller performs:
- Learning MAC-to-port mappings (Learning Switch)
- Handling `packet_in` events
- Installing flow rules (match-action)
- Tracking packet traversal across switches
- Displaying the full path from source to destination

---

## 🌐 Network Topology

Linear topology with 4 switches and 4 hosts:


### 📷 Topology Screenshot
![Topology](images/topology.png)

---

## ▶️ How to Run

### Step 1: Start POX Controller
```bash
cd ~/pox
./pox.py forwarding.l2_learning misc.path_tracer

Step 2: Start Mininet
sudo mn --controller=remote --topo linear,4
Step 3: Test Connectivity
pingall
h1 ping h4
🧪 Test Results
✅ 1. Network Connectivity Test
pingall

📷 Output:


✔ Result: 0% packet loss

✅ 2. End-to-End Communication
h1 ping -c 3 h4

📷 Output:


✔ Result: Successful communication across multiple switches

📊 Path Tracing Output

The controller logs the path taken by packets:

s1 → s2 → s3 → s4
PATH: h1 → s1 → s2 → s3 → s4 → h4
