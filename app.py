import tkinter as tk
import tkinter.ttk as ttk
import BAC0
import threading
import re


# Initialize BAC0
bacnet = BAC0.lite()

def perform_global_scan():
    def run_scan():
        bacnet.whois(global_broadcast=True)
        devices = bacnet.devices
        results = [(str(device),) for device in devices]  # Convert each device to a tuple
        root.after(0, update_results, results)

    threading.Thread(target=run_scan).start()

def perform_range_scan(low_limit, high_limit):
    def run_scan():
        bacnet.whois(f'{low_limit} {high_limit}')
        devices = [(dev[0], dev[1], dev[2], dev[3]) for dev in bacnet.devices]
        root.after(0, update_results, devices)

    threading.Thread(target=run_scan).start()


def on_double_click(event):
    item = tree.selection()[0]
    device_str = tree.item(item, 'values')[0]

    # Use regex to split the string into parts
    regex_pattern = r"\('(.*?)', '(.*?)', '(.*?)', (\d+)\)"
    match = re.match(regex_pattern, device_str)
    if match:
        name, vendor, device_address, device_instance = match.groups()

        # Perform the BAC0 read operation
        # The device_instance is already an integer thanks to the regex
        objects = bacnet.read(f"{device_address} device {device_instance} objectList")
        results_text.insert(tk.END, str(objects) + "\n")
    else:
        print("Invalid device format:", device_str)


def update_results(devices):
    tree.delete(*tree.get_children())  # Clear existing entries
    for device in devices:
        # Ensure the tuple has four elements, using placeholders if necessary
        padded_device = device + ('', '') if len(device) < 4 else device
        tree.insert('', 'end', values=padded_device)

# Set up the Tkinter GUI
root = tk.Tk()
root.title("BACnet Scanner")

# Optionally, set the initial size of the window (width x height)
# root.geometry('800x600')  # Example: 800 pixels wide and 600 pixels tall

# Treeview for displaying BACnet devices
tree = ttk.Treeview(root, columns=['Device Info'], show='headings')
tree.heading('Device Info', text='Device Info')

# Set the width of the 'Device Info' column
tree.column('Device Info', width=500)  # Example: 500 pixels wide

tree.bind("<Double-1>", on_double_click)
tree.pack(expand=True, fill='both')  # Allow the Treeview to expand and fill the window


# Global scan button
global_scan_button = tk.Button(root, text="Global BACnet Scan", command=perform_global_scan)
global_scan_button.pack()

# Range scan inputs and button
low_limit_label = tk.Label(root, text="Low Limit")
low_limit_label.pack()
low_limit_entry = tk.Entry(root)
low_limit_entry.pack()

high_limit_label = tk.Label(root, text="High Limit")
high_limit_label.pack()
high_limit_entry = tk.Entry(root)
high_limit_entry.pack()

range_scan_button = tk.Button(root, text="Range BACnet Scan", command=lambda: perform_range_scan(low_limit_entry.get(), high_limit_entry.get()))
range_scan_button.pack()

# Text area for displaying additional information
results_text = tk.Text(root)
results_text.pack()

# Start the GUI
root.mainloop()
