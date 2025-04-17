import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import datetime
import threading
import time
from matplotlib import dates as mdates

# Global variables
log_file = "server_log.txt"
normal_traffic = []
dos_traffic = []
times = []
server_running = False
attack_started = False
server_crashed = False
max_requests = 500


#=====================================================================================#
#============================> Tkinter window and the Chart <=========================#

# Setting up the Tkinter window
root = tk.Tk()
root.title("Live DoS Monitoring - Server")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{int(screen_width*1)}x{int(screen_height*0.9)}")

#chart
fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(expand=True, fill="both", pady=10)

# Server status
status_label = tk.Label(root, text="🟢 Server is Idle", font=("Arial", 20, "bold"), fg="green")
status_label.pack(pady=5)




#=====================================================================================#
#==================================> Main Fuctions <=================================#

# Update drawing  
def update_plot():
    ax.clear()
    ax.set_title("Traffic Monitoring")
    ax.set_xlabel("Time")
    ax.set_ylabel("Requests/sec")

    ax.set_facecolor('white') 

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

    if normal_traffic:
        filtered_times = [t for t, val in zip(times, normal_traffic) if val is not None]
        filtered_vals = [val for val in normal_traffic if val is not None]
        ax.plot(filtered_times, filtered_vals, 'go-', label="Normal Traffic")

    if attack_started:
        ax.plot(times[:len(dos_traffic)], dos_traffic, 'rX--', label="DoS Attack")

    if server_crashed:
        ax.set_facecolor('#ffe5e5') 
        ax.text(0.5, 0.6, "SERVER CRASHED",
                color='red', fontsize=34, fontweight='bold',
                ha='center', va='center', transform=ax.transAxes)
        ax.text(0.5, 0.4, "Too Many Requests!",
                color='darkred', fontsize=20,
                ha='center', va='center', transform=ax.transAxes)

    ax.legend()
    canvas.draw()

# GENERATING NORMAL TRAFFIC
def generate_normal_traffic():
    global server_running, normal_traffic, times, status_label

    current_requests = random.choice([0, 1])  
    status_label.config(text="🟢 Normal Traffic Running", fg="blue", font=("Arial", 20, "bold"))

    while server_running and not attack_started:
        now = datetime.datetime.now()
        times.append(now)

        user_type = random.choice(["low", "medium", "high"])
        if user_type == "low":
            change = random.randint(-2, 2)
        elif user_type == "medium":
            change = random.randint(-3, 4)
        else:
            change = random.randint(-4, 5)

        current_requests = max(0, min(30, current_requests + change))
        normal_traffic.append(current_requests)
        log_request(current_requests, "Normal")
        update_plot()
        time.sleep(1)

# GENERATING THE DoS Attack
def generate_dos_attack():
    global attack_started, dos_traffic, times, server_crashed, status_label

    attack_started = True
    status_label.config(text="🚨 DoS Attack Running", fg="darkred", font=("Arial", 20, "bold"))

    start_value = normal_traffic[-1] if normal_traffic else 0
    dos_traffic.clear()
    dos_traffic.extend(normal_traffic)

    current_requests = start_value

    while not server_crashed and server_running:
        now = datetime.datetime.now()
        times.append(now)

        current_requests += 25
        dos_traffic.append(current_requests)
        log_request(current_requests, "DoS")
        normal_traffic.append(None)

        update_plot()

        if current_requests >= max_requests:
            server_crashed = True
            status_label.config(text="❌ Server Crashed due to attack!", fg="red")
            update_plot()
            break

        time.sleep(0.5)

def log_request(request_count, traffic_type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {traffic_type}: {request_count} requests\n"
    with open(log_file, "a") as file:
        file.write(log_entry)


#=====================================================================================#
#============================> Buttons Functions and Styles <=========================#
# STARTING Normal Traffic
def start_normal_traffic():
    global server_running, normal_traffic, dos_traffic, times, attack_started, server_crashed
    if not server_running:
        server_running = True
        attack_started = False
        server_crashed = False
        open(log_file, "w").write("=== Server Log Started ===\n")
        normal_traffic.clear()
        dos_traffic.clear()
        times.clear()
        status_label.config(text="🟢 Server is Running", fg="green", font=("Arial", 20, "bold"))
        threading.Thread(target=generate_normal_traffic, daemon=True).start()

# STARTING DoS Attack
def start_dos_attack():
    if server_running and not attack_started:
        threading.Thread(target=generate_dos_attack, daemon=True).start()

# Restarting The Server
def restart_server():
    global server_running
    server_running = False
    time.sleep(1)
    start_normal_traffic()

# Stopping The Server
def stop_server():
    global server_running
    server_running = False
    update_plot()
    status_label.config(text="🛑 Server Stopped", fg="black", font=("Arial", 20, "bold"))
#

button_frame = tk.Frame(root)
button_frame.pack(pady=30)

button_font = ("Arial", 18, "bold")
button_width = 20

btn_start = tk.Button(button_frame, text="👥 Start Normal Clients",
                      command=start_normal_traffic, bg="#c8f7c5",
                      font=button_font, width=button_width, height=2)
btn_start.grid(row=0, column=0, padx=10, pady=10)

btn_attack = tk.Button(button_frame, text="💣 Launch DoS Attack",
                       command=start_dos_attack, bg="#f8d7da",
                       font=button_font, width=button_width, height=2)
btn_attack.grid(row=0, column=1, padx=10, pady=10)

btn_restart = tk.Button(button_frame, text="🔁 Restart Server",
                        command=restart_server, bg="#fff3cd",
                        font=button_font, width=button_width, height=2)
btn_restart.grid(row=0, column=2, padx=10, pady=10)

btn_stop = tk.Button(button_frame, text="⛔ Stop Server",
                     command=stop_server, bg="#e0e0e0",
                     font=button_font, width=button_width, height=2)
btn_stop.grid(row=0, column=3, padx=10, pady=10)



# شريط عرض الإحصائيات
stats_frame = tk.Frame(root)
stats_frame.pack(pady=10)

label_total = tk.Label(stats_frame, text="📦 Total Requests: 0", font=("Arial", 12))
label_total.grid(row=0, column=0, padx=10)

label_dos = tk.Label(stats_frame, text="💣 DoS Requests: 0", font=("Arial", 12))
label_dos.grid(row=0, column=1, padx=10)

label_avg = tk.Label(stats_frame, text="📈 Avg Normal Traffic: 0", font=("Arial", 12))
label_avg.grid(row=0, column=2, padx=10)




root.mainloop()
