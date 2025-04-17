# Denial of Service (DoS) Attack Simulation

## Project Overview
This project simulates a Denial of Service (DoS) attack on a server using Python, featuring a graphical user interface (GUI) developed with Tkinter. The simulation showcases normal server traffic, DoS attack traffic, and the impact of excessive traffic on server stability. The project was developed as part of the "Modeling and Simulation" course.

## Project Features

- Real-Time Traffic Monitoring:
  The project tracks and visualizes server traffic in real-time. Normal traffic and attack traffic are displayed on a live graph.
  
- DoS Attack Simulation: 
  The server experiences a DoS attack when an overwhelming number of requests are sent. The simulation shows how the server's performance degrades until it crashes.
  
- Server Control Buttons:
  The user can start normal traffic, launch a DoS attack, restart the server, or stop the server via simple buttons in the GUI.
  
- Server Crash Simulation: 
  The server crashes once the traffic exceeds a defined limit (maximum requests), simulating the effects of a DoS attack.

## Technologies Used
- Python 3.x
- Tkinter (for GUI)
- Matplotlib (for real-time data plotting)
- Threading (for simulating concurrent traffic and attacks)

## Project Structure
```plaintext
/DoS_Simulation_Project
│
├── /assets            # Contains graphical assets
├── /src               # Source code of the simulation
│   ├── server.py      # Code to simulate server behavior / Main script to run the simulation
│   ├── dos_attack.py  # Logic for simulating DoS attack
│   └── client.py      # Simulating normal traffic and client requests
│
└── README.md          # Project overview and instructions
