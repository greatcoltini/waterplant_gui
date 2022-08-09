import time
import re
import datetime
from main import window


def determine_analyzers(plant_analyzers, finalize_button, analyzer_page):
    current_time = get_time()

    print(plant_analyzers)
    for analyzer in plant_analyzers[:]:
        reading_file = open("plant_database.pf", "r")
        for line in reading_file:
            individual_lines = line.split("\t")
            analyzer_in_database = individual_lines[1]
            analyzer_date = individual_lines[0]
            print(analyzer_date + ":" + current_time[:-1] + ":" + analyzer)

            # if date is equal to current date, remove analyzer option
            if analyzer_date == current_time[:-1] and analyzer_in_database == analyzer:
                delete_analyzer(analyzer)
                break
    if not plant_analyzers:
        finalize_button.destroy()
        analyzer_page.remove(finalize_button)
        exhausted_push()


# Submit the analyzer information to a file
def submit_analyzers(plant_file, finalize_button, analyzer_submit_button):
    plant_file.close()

    if finalize_button:
        finalize_button.config(state="disabled", text="Outputting...")
        analyzer_submit_button.config(state="disabled")

    window.update()
    time.sleep(1)

    exhausted_push()

    change_state(2)


# Method to write information inputted by user
def write_analyzer():

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


# Command that changes the states upon button press
def change_state(event):
    for page in pages:
        state_switch(True, page)
    state_switch(False, pages[event])

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
