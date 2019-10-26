import csv
from tkinter import *
from tkinter import filedialog as fd
from matplotlib import pyplot as plt
import os
from copy import deepcopy

root = Tk()

main_frame = Frame(root)
browse_frame = Frame(main_frame)
info_frame = Frame(main_frame)

header_array = []
checked_dict = {}

for frame in [main_frame, browse_frame, info_frame]:
    frame.pack(expand = True, fill = "both", side = "left")

def apply_settings(f_data_logger, f_date_index, f_time_index):
    index_array = []
    dir_name = fd.askdirectory()
    print(dir_name)
    if dir_name:
        for (key, value) in checked_dict.items():
            if value.get() == 1:
                print(key)
                # print(value.get())
                for element in header_array:
                    if key == element:
                        index_array.append(header_array.index(element))
        for index in index_array:
            values_array = []
            time_array = []
            for row in f_data_logger:
                values_array.append(float(row[index]))
                time_array.append(row[f_time_index])
            plt.plot(time_array, values_array)
            plt.xlabel(header_array[f_time_index])
            plt.ylabel(header_array[index])
            graph_filename = dir_name + "/" + header_array[index]
            plt.savefig(graph_filename, bbox_inches="tight")
            plt.clf()
        print(index_array)
        # plot graph
        # print(graph_filename)
    else:
        print("Please select an output directory")

def open_csv_file():
    for widget in info_frame.winfo_children():
        widget.destroy()

    csv_filename = fd.askopenfilename(initialdir = root, title = "Select CSV file", filetypes = (("CSV files", "*.csv"), ("all files", "*.*")))

    if csv_filename:
        row_number = 0
        num_of_rows = 0

        header_window = Toplevel(root)
        header_frame = Frame(header_window)
        apply_frame = Frame(header_window)
        for frame in [header_frame, apply_frame]:
            frame.pack(expand = True, fill = "both", side = "left")

        # apply_button = Button(apply_frame, text = "Apply", command = lambda: apply_settings(data_logger))
        # apply_button.pack(side = "bottom")
        g_data_logger = []

        with open(csv_filename) as csv_file:
            data_logger = csv.reader(csv_file, delimiter = ",")
            g_data_logger = deepcopy(list(data_logger))
            g_data_logger = g_data_logger[1:-2]
            csv_file.seek(0)
            date_index = 0
            time_index = 0

            for row in data_logger:
                if row_number == 0:
                    for element in row:
                        # print(element)
                        if element:# and element != "Date" and element != "Time":
                            header_array.append(element)
                        if element == "Date":
                            date_index = row.index(element)
                        if element == "Time":
                            time_index = row.index(element)
                row_number += 1
            # print(time_index)
            # print(date_index)
            num_of_rows = row_number
            row_number = 0
            csv_file.seek(0)

        apply_button = Button(apply_frame, text = "Apply", command = lambda: apply_settings(g_data_logger, date_index, time_index))
        apply_button.pack(side = "bottom")

        number_row = 0
        number_column = 0
        for item in header_array:
            if item != "Date" and item != "Time":
                checked_var = IntVar()
                if number_row == 20:
                    number_row = 0
                    number_column += 1
                Checkbutton(header_frame, text = item, variable = checked_var).grid(row = number_row, column = number_column)
                checked_dict.update({item:checked_var})
                number_row += 1
    else:
        info_label = Label(info_frame, text = "File not selected")
        info_label.pack(side = "left")

browse_button = Button(browse_frame, text = "Browse", command = open_csv_file)
browse_button.pack(side = "left")

def on_closing():
    plt.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
