import datetime
import tkinter as tk
from tkinter import ttk
import time
import re

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

CURRENT_STATE = ""


# Function to determine if we have done our daily analyzer checks yet..
# TODO change this to half a day ?
def determine_analyzers():
    current_time = get_time()

    for analyzer in PLANT_ANALYZERS[:]:
        reading_file = open("plant_database.pf", "r")
        for line in reading_file:
            individual_lines = line.split("\t")
            analyzer_in_database = individual_lines[1]
            analyzer_date = individual_lines[0]
            print(analyzer_date + ":" + current_time[:-1] + ":" + analyzer)

            # if date is equal to current date, remove analyzer option
            if analyzer_date == current_time[:-1] and analyzer_in_database == analyzer:
                delete_analyzer(analyzer)

    if not PLANT_ANALYZERS:
        finalize_button.destroy()
        analyzer_page.remove(finalize_button)
        main_residual_btn.config(text="Daily Analyzers Done...", state="disabled")
        exhausted_push()
    else:
        counter = 3 - len(PLANT_ANALYZERS)
        main_residual_btn_text = "Daily Analyzers Done: (" + str(counter) + "/3)"
        main_residual_btn.config(text=main_residual_btn_text, state="enabled", command=lambda: change_state(1))


# Submit the analyzer information to a file
def submit_analyzers():
    plant_file.close()

    if finalize_button:
        finalize_button.config(state="disabled", text="Outputting...")
        analyzer_submit_button.config(state="disabled")

    window.update()
    time.sleep(1)

    exhausted_push()

    change_state(2)


# Method to write information inputted by user
def write_analyzer(menu):

    # check for proper usage of entries
    proper_entry = True

    analyzer_info = [analyzer_name_entry, analyzer_reading_entry, analyzer_recording1_entry,
                     analyzer_recording2_entry]

    counter = 0
    for entry in analyzer_info:
        if counter > 0:
            if re.match("^\d\.\d{2}$", entry.get()):
                pass
            else:
                entry.delete(0, tk.END)
                entry.insert(0, "Must be of the form: #.## | 1.23")
                proper_entry = False
        counter += 1

    if proper_entry:
        analyzer_string = ""
        analyzer_string += get_time()
        for info in analyzer_info:
            analyzer_string += info.get() + "\t"
        plant_file.write(analyzer_string + "\n")

        for info in analyzer_info:
            info.delete(0, tk.END)

        delete_analyzer(analyzer_name_entry.get())

        finalize_button.config(state="active")

        change_state(1)
    else:
        pass


# Delete analyzer function
def delete_analyzer(analyzer):
    for item in PLANT_ANALYZERS:
        if item == analyzer:
            analyzer_menu['menu'].delete(item)
            PLANT_ANALYZERS.remove(item)
    if len(PLANT_ANALYZERS) > 0:
        plant_analyzers_var.set(PLANT_ANALYZERS[0])
        change_analyzer(0)
    else:
        exhausted_push()


# function to call for submission of residual to file.
def submit_residual():
    # variable initialization
    proper_date = True
    proper_value = True
    residual_info = [residual_location_entry, residual_time_entry, residual_value_entry]
    residual_file = open("residuals.txt", 'a')

    # regex for time and value
    if not re.match("^\d\d:\d\d$", residual_time_entry.get()):
        proper_date = False
        residual_time_entry.delete(0, tk.END)
        residual_time_entry.insert(0, "Must be hh:mm...")

    if not re.match("^\d\.\d{2}$", residual_value_entry.get()):
        proper_value = False
        residual_value_entry.delete(0, tk.END)
        residual_value_entry.insert(0, "Must be #.##")

    if proper_date and proper_value:
        residual_string = ""
        residual_string += get_time()
        for item in residual_info:
            residual_string += item.get() + "\t"
        residual_file.write(residual_string + "\n")

        for item in residual_info:
            item.delete(0, tk.END)
    else:
        pass


# display previous residuals
def previous_residuals():
    pass


# get time and return it in format for writing
def get_time():
    current_time = datetime.datetime.now()
    return str(current_time.year) + "/" + str(current_time.month) + "/" + str(current_time.day) + "\t"


# Clears out button for pushing, and analyzer menu
def exhausted_push():
    analyzer_label.config(text="All analyzers entered for the day.", height=10, borderwidth=4, relief="groove")
    for item in analyzer_page[:]:
        if item == display_previous_recordings or item == finalize_button or item == analyzer_label:
            pass
        else:
            item.destroy()
            analyzer_page.remove(item)


# configures analyzer to change
def change_analyzer(event):
    analyzer_name_entry.config(state="normal")
    analyzer_name_entry.delete(0, tk.END)
    analyzer_name_entry.insert(0, plant_analyzers_var.get())
    analyzer_name_entry.config(state="readonly")


# Reverts the state when the back button is pressed
def return_previous_page():
    if CURRENT_STATE == analyzer_previous_page:
        change_state(1)
    elif CURRENT_STATE == previous_residuals_page:
        change_state(3)


# Command that changes the states upon button press
def change_state(event):
    for page in pages:
        state_switch(True, page)
    state_switch(False, pages[event])

    global CURRENT_STATE
    CURRENT_STATE = pages[event]

    if event == 2:
        table_generation()


# Controls the state of the required page
def state_switch(state, page):
    if state:
        for item in page:
            item.pack_forget()
    else:
        for item in page:
            item.pack()


def daily_completed():
    if PLANT_ANALYZERS:
        counter = 3 - len(PLANT_ANALYZERS)
        main_residual_btn_text = "Daily Analyzers Done: (" + str(counter) + "/3)"
        main_residual_btn.config(text=main_residual_btn_text)


# Table generation
# OPENS THE GENERATED PLANT FILE FOR ANALYZERS
# READS THEM INTO A TABLE BASED ON DATE
# COLUMN FOR DATE | ANALYZER NAME | READING | RESIDUAL 1 | RESIDUAL 2
def table_generation():
    # necessary to refresh table
    analyzer_table.delete(*analyzer_table.get_children())

    analyzer_data = open("plant_database.pf", "r")
    analyzer_table['columns'] = ('Date', 'Analyzer', 'Reading', 'Residual 1', 'Residual 2')

    # format our column
    analyzer_table.column("#0", width=0, stretch=tk.NO)
    analyzer_table.column("Date", anchor=tk.CENTER, width=80)
    analyzer_table.column("Analyzer", anchor=tk.CENTER, width=80)
    analyzer_table.column("Reading", anchor=tk.CENTER, width=80)
    analyzer_table.column("Residual 1", anchor=tk.CENTER, width=80)
    analyzer_table.column("Residual 2", anchor=tk.CENTER, width=80)

    # Create Headings
    analyzer_table.heading("#0", text="", anchor=tk.CENTER)
    analyzer_table.heading("Date", text="Date", anchor=tk.CENTER)
    analyzer_table.heading("Analyzer", text="Analyzer", anchor=tk.CENTER)
    analyzer_table.heading("Reading", text="Reading", anchor=tk.CENTER)
    analyzer_table.heading("Residual 1", text="Residual 1", anchor=tk.CENTER)
    analyzer_table.heading("Residual 2", text="Residual 2", anchor=tk.CENTER)

    counter = 0
    for line in analyzer_data:
        section = line.split("\t")
        analyzer_table.insert(parent='', index='end', iid=str(counter), text='', values=(section[0], section[1], section[2],
                                                                                section[3], section[4]))
        counter += 1

    analyzer_table.pack()
    analyzer_data.close()


# Generation of the GUI for the water plant
window = tk.Tk()
window.title("Water Plant GUI")
window.geometry('480x360')
window.grid_columnconfigure((0,1), weight=1)

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
    label="Main Page",
    command=lambda: change_state(5)
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
analyzer_recording1_entry.insert(0, "Enter first residual.")
analyzer_recording1_entry.bind('<FocusIn>', lambda x: analyzer_recording1_entry.selection_range(0, tk.END))
analyzer_recording1_entry.pack()

analyzer_recording2_entry = tk.Entry(selectborderwidth=2, width=30, justify="center")
analyzer_recording2_entry.insert(0, "Enter second residual.")
analyzer_recording2_entry.bind('<FocusIn>', lambda x: analyzer_recording2_entry.selection_range(0, tk.END))
analyzer_recording2_entry.pack()

analyzer_submit_button = tk.Button(text="Push Analyzer", command=lambda: [write_analyzer(analyzer_menu), daily_completed()])
analyzer_submit_button.pack()

finalize_button = tk.Button(text="Finalize", command=submit_analyzers, state="disabled")
finalize_button.pack()

plant_analyzers_var = tk.StringVar()
plant_analyzers_var.set(PLANT_ANALYZERS[0])

analyzer_menu = tk.OptionMenu(window, plant_analyzers_var, *PLANT_ANALYZERS, command=change_analyzer)
analyzer_menu.pack()

display_previous_recordings = tk.Button(text="Show Previous Recordings", command=lambda: change_state(2))
display_previous_recordings.pack()


# components for analyzer history page
analyzer_table = ttk.Treeview(window)
back_button = tk.Button(text="Back", command=lambda: return_previous_page())

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
previous_residual_button = tk.Button(residuals_frame, text="Residuals Table", command=lambda: change_state(4))


# creation of main page...
main_frame1 = ttk.Frame(window)

# grid layout
main_frame1.columnconfigure(0, weight=1)
main_frame1.columnconfigure(0, weight=5)
main_label = tk.Label(main_frame1, text="Main Page", borderwidth=4, relief="groove", height=5, width=20)
main_residual_btn = ttk.Button(main_frame1, text="Daily Residuals")
main_plant_walkthru = ttk.Button(main_frame1, text="Plant Walkthrough")
main_uv_anal = ttk.Button(main_frame1, text="UV Analyzers")
main_checks = ttk.Button(main_frame1, text="Locational Residuals", command=lambda: change_state(3))


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

previous_residuals_page = [
    back_button
]

main_page = [
    main_frame1,
    main_label,
    main_residual_btn,
    main_plant_walkthru,
    main_uv_anal,
    main_checks
]

# container of all containers
pages = [
    uv_page,
    analyzer_page,
    analyzer_previous_page,
    residuals_page,
    previous_residuals_page,
    main_page
]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    determine_analyzers()
    change_state(5)
    window.mainloop()


