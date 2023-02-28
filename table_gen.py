import tkinter as tk
# UV Table generation
# OPENS THE GENERATED LAMP FILE
# READS THEM INTO A TABLE BASED ON DATE
# COLUMN FOR DATE | REACTOR | LAMP | SN | NET HRS | NET CYCLES
def lamp_table_generation(lamp_table):
    # necessary to refresh table
    lamp_table.delete(*lamp_table.get_children())

    lamp_data = open("lamp_database.pf", "r")
    lamp_table['columns'] = ('Date', 'Reactor', 'Lamp', 'Serial #', 'Net Hours', 'Net Cycles')

    # format our column
    lamp_table.column("#0", width=0, stretch=tk.NO)
    lamp_table.column("Date", anchor=tk.CENTER, width=20)
    lamp_table.column("Reactor", anchor=tk.CENTER, width=10)
    lamp_table.column("Lamp", anchor=tk.CENTER, width=10)
    lamp_table.column("Serial #", anchor=tk.CENTER, width=80)
    lamp_table.column("Net Hours", anchor=tk.CENTER, width=20)
    lamp_table.column("Net Cycles", anchor=tk.CENTER, width=20)
    
    # Create Headings
    lamp_table.heading("#0", text="", anchor=tk.CENTER)
    lamp_table.heading("Date", text="Date", anchor=tk.CENTER, sort_by='date')
    lamp_table.heading("Reactor", text="Reactor", anchor=tk.CENTER, sort_by='multidecimal')
    lamp_table.heading("Lamp", text="Lamp", anchor=tk.CENTER, sort_by='multidecimal')
    lamp_table.heading("Serial #", text="Serial #", anchor=tk.CENTER, sort_by='multidecimal')
    lamp_table.heading("Net Hours", text="Net Hours", anchor=tk.CENTER, sort_by='multidecimal')
    lamp_table.heading("Net Cycles", text="Net Cycles", anchor=tk.CENTER, sort_by='multidecimal')


    counter = 0
    for line in lamp_data:
        section = line.split("\t")
        lamp_table.insert(parent='', index='end', iid=str(counter), text='', values=(section[3], section[0], section[1],
                                                                                section[2], section[4], section[5]))
        counter += 1

    lamp_table.pack()
    lamp_data.close()

