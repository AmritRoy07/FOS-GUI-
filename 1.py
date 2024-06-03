import tkinter as tk
from tkinter import messagebox
import numpy as np

def calculate_FOS(event=None):
    try:
        coh_act = float(entries[0].get())
        phi_act = float(entries[1].get())
        gamma_act = float(entries[2].get())
        kh_act = float(entries[3].get())

        # Define valid ranges
        coh_min, coh_max = 809.77, 1195.17
        phi_min, phi_max = 35.18, 49.40
        gamma_min, gamma_max = 22.02, 25.99
        kh_min, kh_max = 0, 0.20
        FOS_min, FOS_max = 1.311, 2.864

        # Check input ranges
        if not (coh_min <= coh_act <= coh_max and phi_min <= phi_act <= phi_max and gamma_min <= gamma_act <= gamma_max and kh_min <= kh_act <= kh_max):
            messages.insert('end', "Use valid range for input values.\n")
            return

        if len(str(kh_act).split('.')[1]) < 2:
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

        output_var.set(f"{FOS[0]:.3f}")
        messages.insert('end', "Estimation Of FOC of Mount St. Helens Completed.\n")
    except ValueError:
        pass

# Create the main window
root = tk.Tk()
root.title("FOS Estimator of Mount St. Helens")

# Create input parameter labels and entry fields
labels = ["Cohesion (c, kN/m²)", "Angle of internal friction (Ø, °)", "Unit weight (γ, kN/m³)", "Seismic coefficient (ke, -)"]
valid_ranges = ["(809.77 to 1195.17)", "(35.18 to 49.40)", "(22.02 to 25.99)", "(0 to 0.20)"]
entries = []

for i, (label, valid_range) in enumerate(zip(labels, valid_ranges)):
    tk.Label(root, text=label).grid(row=i, column=0)
    tk.Label(root, text=valid_range).grid(row=i, column=2)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1)
    entries.append(entry)

# Create a button to calculate FOS
calculate_button = tk.Button(root, text="Calculate FOS", command=calculate_FOS)
calculate_button.grid(row=len(labels), column=0, columnspan=3)

# Create a label to display the result
output_var = tk.StringVar()
result_label = tk.Label(root, textvariable=output_var)
result_label.grid(row=len(labels)+1, column=0, columnspan=3)

# Create a text widget for messages
messages = tk.Text(root, height=5, width=50)
messages.grid(row=len(labels)+2, column=0, columnspan=3)

# Run the main event loop
root.mainloop()
