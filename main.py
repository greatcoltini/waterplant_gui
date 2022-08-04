import datetime
import tkinter as tk
import os
import time

plant_file = open("plant_database.pf", "w")
current_time = datetime.datetime.now()
plant_file.write(str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "\n")

def submit_analyzers():
    plant_file.close()

    analyzer_submit_button.config(state="disabled", text="Outputting...")

    time.sleep(2.5)

    os.startfile("plant_database.pf")

def write_analyzer():
    a_name = analyzer_name_entry.get()
    a_reading = analyzer_reading_entry.get()
    a_r1 = analyzer_recording1_entry.get()
    a_r2 = analyzer_recording2_entry.get()
    plant_file.write(a_name + "\t" + a_reading + "\t" + a_r1 + "\t" + a_r2 + "\n")


# Generation of the GUI for the water plant
window = tk.Tk()
window.title("Water Plant GUI")

opening_label = tk.Label(text="Welcome to your Plant Operations GUI")
opening_label.pack()

analyzer_label = tk.Label(text="Enter your analyzer information here.")
analyzer_label.pack()

analyzer_name_entry = tk.Entry(selectborderwidth=2, width=30)
analyzer_name_entry.insert(0, "Enter analyzer name here.")
analyzer_name_entry.pack()

analyzer_reading_entry = tk.Entry(selectborderwidth=2, width=30)
analyzer_reading_entry.insert(0, "Enter analyzer reading.")
analyzer_reading_entry.bind('<FocusIn>', lambda x: analyzer_reading_entry.selection_range(0, tk.END))
analyzer_reading_entry.pack()

analyzer_recording1_entry = tk.Entry(selectborderwidth=2, width=30)
analyzer_recording1_entry.insert(0, "Enter first recording reading.")
analyzer_recording1_entry.pack()

analyzer_recording2_entry = tk.Entry(selectborderwidth=2, width=30)
analyzer_recording2_entry.insert(0, "Enter second recording reading.")
analyzer_recording2_entry.pack()

analyzer_submit_button = tk.Button(text="Push Analyzer", command=write_analyzer)
analyzer_submit_button.pack()

finalize_button = tk.Button(text="Finalize", command=submit_analyzers)
finalize_button.pack()

window.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
