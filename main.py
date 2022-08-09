import tkinter as tk
from tkinter import ttk
from utils import *

plant_file = open("plant_database.pf", "a")

PLANT_ANALYZERS = [
    "UV-AIT3",
    "HL-AIT2",
    "HL-AIT6"
]

GUI_STATE = [
    "analyzers",
    "uv"
]


# Function to determine if we have done our daily analyzer checks yet..
# TODO change this to half a day ?


# Generation of the GUI for the water plant
window = tk.Tk()
window.title("Water Plant GUI")
window.geometry('480x360')

nav_menu = tk.Menu(window)
window.config(menu=nav_menu)

nav_menu.add_command(
    label="UV Reactor Outline",
    command=lambda: change_state(0)
)
nav_menu.add_command(
    label="Analyzer Readings",
    command=lambda: change_state(1)
)
nav_menu.add_command(
    label="Residual Information",
    command=lambda: change_state(3)
)
nav_menu.add_command(
    label="Help",
    command=lambda: change_state(0)
)
nav_menu.add_command(
    label="Exit",
    command=window.destroy
)

opening_label = tk.Label(text="Welcome to your Plant Operations GUI")
opening_label.pack()

analyzer_label = tk.Label(text="Enter your analyzer information here.")
analyzer_label.pack()

analyzer_name_entry = tk.Entry(selectborderwidth=2, width=30, justify="center")
analyzer_name_entry.insert(0, PLANT_ANALYZERS[0])
analyzer_name_entry.bind('<FocusIn>', lambda: analyzer_name_entry.selection_range(0, tk.END))
analyzer_name_entry.config(state="readonly")
analyzer_name_entry.pack()

analyzer_reading_entry = tk.Entry(selectborderwidth=2, width=30, justify="center")
analyzer_reading_entry.insert(0, "Enter analyzer reading.")
analyzer_reading_entry.bind('<FocusIn>', lambda: analyzer_reading_entry.selection_range(0, tk.END))
analyzer_reading_entry.pack()

analyzer_recording1_entry = tk.Entry(selectborderwidth=2, width=30, justify='center')
analyzer_recording1_entry.insert(0, "Enter first residual.")
analyzer_recording1_entry.bind('<FocusIn>', lambda: analyzer_recording1_entry.selection_range(0, tk.END))
analyzer_recording1_entry.pack()

analyzer_recording2_entry = tk.Entry(selectborderwidth=2, width=30, justify="center")
analyzer_recording2_entry.insert(0, "Enter second residual.")
analyzer_recording2_entry.bind('<FocusIn>', lambda: analyzer_recording2_entry.selection_range(0, tk.END))
analyzer_recording2_entry.pack()

analyzer_submit_button = tk.Button(text="Push Analyzer", command=lambda: write_analyzer())
analyzer_submit_button.pack()

finalize_button = tk.Button(text="Finalize", command=lambda: submit_analyzers(
    plant_file, finalize_button, analyzer_submit_button), state="disabled")
finalize_button.pack()

plant_analyzers_var = tk.StringVar()
plant_analyzers_var.set(PLANT_ANALYZERS[0])

analyzer_menu = tk.OptionMenu(window, plant_analyzers_var, *PLANT_ANALYZERS, command=change_analyzer)
analyzer_menu.pack()

display_previous_recordings = tk.Button(text="Show Previous Recordings", command=lambda: change_state(2))
display_previous_recordings.pack()


# components for analyzer history page
analyzer_table = ttk.Treeview(window)
back_button = tk.Button(text="Back", command=lambda: change_state(1))

# components for residual page
residuals_frame = tk.Frame(window)
residual_label = tk.Label(residuals_frame, text="Enter Residuals Here")
residual_location_entry = tk.Entry(residuals_frame, selectborderwidth=2, width=30, justify="center")
residual_location_label = tk.Label(residuals_frame, text="Location:")
residual_time_entry = tk.Entry(residuals_frame, selectborderwidth=2, width=30, justify="center")
residual_time_label = tk.Label(residuals_frame, text="Time:")
residual_value_entry = tk.Entry(residuals_frame, selectborderwidth=2, width=30, justify="center")
residual_value_label = tk.Label(residuals_frame, text="Residual:")
residual_push_button = tk.Button(residuals_frame, text="Submit Residual", command=lambda: submit_residual())
previous_residual_button = tk.Button(residuals_frame, text="Residuals Table", command=lambda: previous_residuals())


# components for residual history page
residual_table = ttk.Treeview(window)

# Container of all analyzer page elements
analyzer_page = [
    analyzer_label,
    analyzer_name_entry,
    analyzer_reading_entry,
    analyzer_recording1_entry,
    analyzer_recording2_entry,
    analyzer_submit_button,
    finalize_button,
    analyzer_label,
    analyzer_menu,
    display_previous_recordings
]

analyzer_previous_page = [
    analyzer_table,
    back_button
]

uv_page = [

]

residuals_page = [
    residuals_frame,
    residual_label,
    residual_location_label,
    residual_location_entry,
    residual_time_label,
    residual_time_entry,
    residual_value_label,
    residual_value_entry,
    residual_push_button,
    previous_residual_button
]


# container of all containers
pages = [
    uv_page,
    analyzer_page,
    analyzer_previous_page,
    residuals_page
]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    determine_analyzers(PLANT_ANALYZERS, finalize_button, analyzer_page)
    window.mainloop()


