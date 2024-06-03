import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np

def calculate_FOS(event=None):
    try:
        coh_act = float(entries_single[0].get())
        phi_act = float(entries_single[1].get())
        gamma_act = float(entries_single[2].get())
        kh_act = float(entries_single[3].get())

        # Define valid ranges
        coh_min, coh_max = 809.77, 1195.17
        phi_min, phi_max = 35.18, 49.40
        gamma_min, gamma_max = 22.02, 25.99
        kh_min, kh_max = 0, 0.20
        FOS_min, FOS_max = 1.311, 2.864

        # Check input ranges
        if not (coh_min <= coh_act <= coh_max and phi_min <= phi_act <= phi_max and gamma_min <= gamma_act <= gamma_max and kh_min <= kh_act <= kh_max):
            messages_single.insert('end', "Use valid range for input values.\n")
            return

        # Define matrices for calculation
        WM1 = np.array([
            [1.2128, 1.1998, -0.0983, 0.0943, 0.4363, -0.3550, -0.4031, -0.8791],
            [1.7655, 0.0843, -0.4341, 0.2536, 2.1245, -0.0737, 1.6471, -2.0288],
            [-0.3319, 1.1062, 0.0289, -0.0084, 0.4660, -0.6024, 1.3598, 0.4425],
            [0.9995, 0.7243, 0.4918, -0.2207, 0.1650, -0.9283, 0.2813, -1.2230]
        ])

        BM1 = np.array([-2.2941, -1.3986, 1.4235, 0.0455, 0.2659, -0.8758, -1.8870, 2.4074])
        WM2 = np.array([-0.0643, -0.0304, -1.1639, 1.3973, 0.0009, 0.0614, 0.0022, -0.0685])
        BM2 = np.array([0.7887])

        # Normalize inputs
        coh_norm = 2 * ((coh_act - coh_min) / (coh_max - coh_min)) - 1
        phi_norm = 2 * ((phi_act - phi_min) / (phi_max - phi_min)) - 1
        gamma_norm = 2 * ((gamma_act - gamma_min) / (gamma_max - gamma_min)) - 1
        kh_norm = 2 * ((kh_act - kh_min) / (kh_max - kh_min)) - 1

        Inputs = np.array([coh_norm, phi_norm, gamma_norm, kh_norm])
        MC1 = np.matmul(Inputs, WM1)
        MC2 = np.add(MC1, BM1)
        MC3 = np.tanh(MC2)
        MC4 = np.matmul(MC3, WM2)
        MC5 = np.add(MC4, BM2)
        FOS = (((MC5 + 1) / 2) * (FOS_max - FOS_min)) + FOS_min

        output_var_single.set(f"{FOS[0]:.3f}")
        messages_single.insert('end', "Estimation Of FOS Completed.\n")
    except ValueError:
        messages_single.insert('end', "Invalid input values.\n")

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the file contains lines of input values in the order: cohesion, phi, gamma, kh
            inputs = data.split('\n')
            for i, input_value in enumerate(inputs):
                entries_single[i].delete(0, tk.END)
                entries_single[i].insert(0, input_value)

def download_results():
    result = output_var_single.get()
    if result:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(f"Estimated FOS: {result}\n")
                messages_single.insert('end', "Results downloaded.\n")
    else:
        messages_single.insert('end', "No results to download.\n")

# Create the main window
root = tk.Tk()
root.title("FOS Estimator of Mount St. Helens")

# Create frames for single and multiple sets of inputs
frame_single = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief='groove')
frame_single.grid(row=0, column=0, padx=10, pady=10, sticky='n')

frame_multiple = tk.Frame(root, padx=10, pady=10, borderwidth=2, relief='groove')
frame_multiple.grid(row=0, column=1, padx=10, pady=10, sticky='n')

# Title for single set of inputs
tk.Label(frame_single, text="Single Set of Inputs", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=10)

# Input fields for single set of inputs
labels = ["Cohesion (c, kN/m²)", "Angle of internal friction (Ø, °)", "Unit weight (γ, kN/m³)", "Seismic coefficient (ke, -)"]
valid_ranges = ["(809.77 to 1195.17)", "(35.18 to 49.40)", "(22.02 to 25.99)", "(0 to 0.20)"]
entries_single = []

for i, (label, valid_range) in enumerate(zip(labels, valid_ranges)):
    tk.Label(frame_single, text=label).grid(row=i+1, column=0)
    tk.Label(frame_single, text=valid_range).grid(row=i+1, column=2)
    entry = tk.Entry(frame_single)
    entry.grid(row=i+1, column=1)
    entries_single.append(entry)

# Create a button to calculate FOS
calculate_button = tk.Button(frame_single, text="Calculate FOS", command=calculate_FOS)
calculate_button.grid(row=len(labels)+1, column=0, columnspan=3, pady=10)

# Create a label to display the result
output_var_single = tk.StringVar()
# Create a frame to contain the result
result_frame = tk.Frame(frame_single, borderwidth=2, relief='groove')
result_frame.grid(row=len(labels)+2, column=0, columnspan=3, pady=5)

# Create a label to display the result
result_label = tk.Label(result_frame, text="Estimated FOS:", font=("Arial", 12))
result_label.pack(side="left")

result_value = tk.Label(result_frame, textvariable=output_var_single, font=("Arial", 12))
result_value.pack(side="right", padx=5, pady=5, expand=True, fill="both")


# Title for multiple sets of inputs
tk.Label(frame_multiple, text="Multiple Sets of Inputs", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

# Create buttons to upload file and download results
upload_button = tk.Button(frame_multiple, text="Upload dataset", command=upload_file)
upload_button.grid(row=1, column=0, columnspan=2, pady=5)

download_button = tk.Button(frame_multiple, text="Estimate and Download", command=download_results)
download_button.grid(row=2, column=0, columnspan=2, pady=5)

# Create a text widget for messages
messages_multiple = tk.Text(frame_multiple, height=5, width=50)
messages_multiple.grid(row=3, column=0, columnspan=2, pady=10, sticky="e")

# Run the main event loop
root.mainloop()
