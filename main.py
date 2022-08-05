import datetime
import tkinter as tk
import os
import time

plant_file = open("plant_database.pf", "w")
current_time = datetime.datetime.now()
plant_file.write(str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "\n")

PLANT_ANALYZERS = [
    "UV-AIT3",
    "HL-AIT2",
    "HL-AIT6"
]

GUI_STATE = [
    "analyzers",
    "uv"
]


# Submit the analyzer information to a file
def submit_analyzers():
    plant_file.close()

    finalize_button.config(state="disabled", text="Outputting...")
    analyzer_submit_button.config(state="disabled")

    window.update()

    time.sleep(1)

    os.startfile("plant_database.pf")


# Method to write information inputted by user
def write_analyzer():
    analyzer_info = [analyzer_name_entry, analyzer_reading_entry, analyzer_recording1_entry,
                     analyzer_recording2_entry]
    analyzer_string = ""
    for info in analyzer_info:
        analyzer_string += info.get() + "\t"
    plant_file.write(analyzer_string + "\n")

    for info in analyzer_info:
        info.delete(0, tk.END)

def changeAnalyzer(event):
    analyzer_name_entry.config(state="normal")
    analyzer_name_entry.delete(0, tk.END)
    analyzer_name_entry.insert(0, plant_analyzers_var.get())
    analyzer_name_entry.config(state="readonly")


def change_state(event):
    if event == 0:
        analyzer_state_switch(True)
    elif event == 1:
        analyzer_state_switch(False)
    else:
        pass


# Controls the analyzer page
def analyzer_state_switch(state):
    if state:
        for item in analyzer_page:
            item.pack_forget()
    else:
        for item in analyzer_page:
            item.pack()

def uv_state_switch(state):
    if state:
        pass

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
    label="Recordings Information",
    command=lambda: change_state(0)
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
analyzer_name_entry.bind('<FocusIn>', lambda x: analyzer_name_entry.selection_range(0, tk.END))
analyzer_name_entry.config(state="readonly")
analyzer_name_entry.pack()

analyzer_reading_entry = tk.Entry(selectborderwidth=2, width=30, justify="center")
analyzer_reading_entry.insert(0, "Enter analyzer reading.")
analyzer_reading_entry.bind('<FocusIn>', lambda x: analyzer_reading_entry.selection_range(0, tk.END))
analyzer_reading_entry.pack()

analyzer_recording1_entry = tk.Entry(selectborderwidth=2, width=30, justify='center')
analyzer_recording1_entry.insert(0, "Enter first recording reading.")
analyzer_recording1_entry.bind('<FocusIn>', lambda x: analyzer_recording1_entry.selection_range(0, tk.END))
analyzer_recording1_entry.pack()

analyzer_recording2_entry = tk.Entry(selectborderwidth=2, width=30, justify="center")
analyzer_recording2_entry.insert(0, "Enter second recording reading.")
analyzer_recording2_entry.bind('<FocusIn>', lambda x: analyzer_recording2_entry.selection_range(0, tk.END))
analyzer_recording2_entry.pack()

analyzer_submit_button = tk.Button(text="Push Analyzer", command=write_analyzer)
analyzer_submit_button.pack()

finalize_button = tk.Button(text="Finalize", command=submit_analyzers)
finalize_button.pack()

plant_analyzers_var = tk.StringVar()
plant_analyzers_var.set(PLANT_ANALYZERS[0])

analyzer_menu = tk.OptionMenu(window, plant_analyzers_var, *PLANT_ANALYZERS, command=changeAnalyzer)
analyzer_menu.pack()

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
    analyzer_menu
]

uv_page = [
    
]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window.mainloop()

