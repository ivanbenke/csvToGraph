import csv
import tkinter as tk
from tkinter import filedialog as fd
from matplotlib import pyplot as plt
from copy import deepcopy
from sys import platform
import os
import re
import time
from datetime import datetime

def _on_close():
    plt.close()
    root.destroy()

def _configure_frame_scrolling(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def _mouse_wheel_handler(event):
    if platform.startswith("linux") or platform.startswith("win32"):
        scroll_count = int(-1*(event.delta/120))
    elif platform.startswith("darwin"):
        scroll_count = int(event.delta)
    header_canvas.yview_scroll(scroll_count, "units")

def _bound_to_mousewheel(event):
    # Windows/Mac
    header_canvas.bind_all("<MouseWheel>", _mouse_wheel_handler)
    # Linux
    header_canvas.bind_all("<Button-4>", _mouse_wheel_handler)
    header_canvas.bind_all("<Button-5>", _mouse_wheel_handler)

def _unbound_to_mousewheel(event):
    # Windows/Mac
    header_canvas.unbind_all("<MouseWheel>")
    # Linux
    header_canvas.unbind_all("<Button-4>")
    header_canvas.unbind_all("<Button-5>")

root = tk.Tk()

main_frame = tk.Frame(root, width="500", height="800")
main_frame.pack(expand = True, fill = "both", side = "left")
main_frame.pack_propagate(0)

search_frame = tk.Frame(main_frame)
search_frame.pack(expand = True, fill = "x", side = "top")

search_entry = tk.Entry(search_frame)
search_entry.pack(expand = True, fill = "x", side = "left")

search_button = tk.Button(search_frame, text = "Search", state = "disabled")
search_button.pack(side = "right")

main_header_frame = tk.Frame(main_frame, width="480", height="700")
main_header_frame.pack(expand = True, fill = "both", side = "top")
main_header_frame.pack_propagate(0)

header_canvas = tk.Canvas(main_header_frame)
header_frame = tk.Frame(header_canvas)
vertical_sb = tk.Scrollbar(main_header_frame, orient="vertical", command=header_canvas.yview)

header_canvas.configure(yscrollcommand=vertical_sb.set)

vertical_sb.pack(fill="y", side="right")

header_canvas.pack(expand = True, fill = "y", side = "left")
header_canvas.create_window((4,4), window=header_frame, anchor="nw")

header_frame.bind("<Configure>", lambda event, canvas=header_canvas: _configure_frame_scrolling(header_canvas))

main_header_frame.bind("<Enter>", _bound_to_mousewheel)
main_header_frame.bind("<Leave>", _unbound_to_mousewheel)

browse_frame = tk.Frame(main_frame)
browse_frame.pack(expand = True, fill = "x", side = "left")
browse_button = tk.Button(browse_frame, text = "Browse")
browse_button.pack(side = "left")

info_frame = tk.Frame(main_frame)
info_frame.pack(expand = True, fill = "x", side = "left")

apply_frame = tk.Frame(main_frame)
apply_frame.pack(expand = True, fill = "x", side = "right")
apply_button = tk.Button(apply_frame, text = "Apply", state = "disabled")
apply_button.pack(side = "right")

header_list_without_units = []
header_list_with_units = []
checked_dict = {}

def populate_checklist(search_term = None):
    for widget in header_frame.winfo_children():
        widget.destroy()

    number_row = 0
    number_column = 0
    if search_term:
        regex_string = r".*" + re.escape(search_term) + r".*"
        for item in header_list_without_units:
            if item != "Date" and item != "Time":
                regex_object = re.search(regex_string, item, re.IGNORECASE)
                if regex_object:
                    checked_var = tk.IntVar()
                    tk.Checkbutton(header_frame, text = regex_object.group(), variable = checked_var).grid(row = number_row, column = number_column, sticky = "w")
                    checked_dict.update({item:checked_var})
                    number_row += 1
    else:
        for item in header_list_without_units:
            if item != "Date" and item != "Time":
                checked_var = tk.IntVar()
                tk.Checkbutton(header_frame, text = item, variable = checked_var).grid(row = number_row, column = number_column, sticky = "w")
                checked_dict.update({item:checked_var})
                number_row += 1

def apply_settings(f_data_logger, f_date_index, f_time_index):
    index_array = []
    dir_name = fd.askdirectory()
    if dir_name:
        for (key, value) in checked_dict.items():
            if value.get() == 1:
                for element in header_list_without_units:
                    if key == element:
                        index_array.append(header_list_without_units.index(element))
        for index in index_array:
            values_array = []
            date_array = []
            time_array = []
            datetime_array = []
            i = 0
            for row in f_data_logger:
                values_array.append(float(row[index]))
                date_array.append(row[f_date_index])
                time_array.append(row[f_time_index][:row[f_time_index].index(".")])
            if len(date_array) == len(time_array):
                for i in range(0, len(date_array)):
                    converted_datetime = time.strptime(date_array[i] + " " + time_array[i], "%d.%m.%Y %H:%M:%S")
                    datetime_array.append(datetime.fromtimestamp(time.mktime(converted_datetime)))
                plt.plot(datetime_array, values_array)
                plt.xlabel(header_list_with_units[f_time_index])
                plt.ylabel(header_list_with_units[index])
                graph_filename = dir_name + "/" + header_list_without_units[index] + ".png"
                if os.path.isfile(graph_filename):
                    os.remove(graph_filename)
                plt.savefig(graph_filename, format = "png", dpi = 300)
                plt.clf()
            else:
                print("Not enough data supplied")
    else:
        print("Please select an output directory")

def search_for_regex(text_input):
    if text_input:
        populate_checklist(text_input)
    else:
        populate_checklist()

def open_csv_file():
    for widget in info_frame.winfo_children():
        widget.destroy()

    csv_filename = fd.askopenfilename(initialdir = root, title = "Select CSV file", filetypes = (("CSV files", "*.csv"), ("all files", "*.*")))

    if csv_filename:
        row_number = 0
        num_of_rows = 0

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
                        if element:
                            header_list_without_units.append(element)
                        if element == "Date":
                            date_index = row.index(element)
                        if element == "Time":
                            time_index = row.index(element)
                row_number += 1
            num_of_rows = row_number
            row_number = 0
            csv_file.seek(0)

        start_index = 0
        end_index = 0
        for item in header_list_without_units:
            header_list_with_units.append(item)
        for i in range(0, len(header_list_without_units)):
            if "/" in header_list_without_units[i]:
                header_list_without_units[i] = header_list_without_units[i].replace("/", " ")
            if "\\" in header_list_without_units[i]:
                header_list_without_units[i] = header_list_without_units[i].replace("\\", " ")
            if "[" in header_list_without_units[i]:
                start_index = header_list_without_units[i].index("[")
            if "]" in header_list_without_units[i]:
                end_index = header_list_without_units[i].index("]")
            if start_index and end_index and end_index > start_index:
                header_list_without_units[i] = header_list_without_units[i].replace(header_list_without_units[i], header_list_without_units[i][:start_index])
                header_list_without_units[i] = header_list_without_units[i].strip()

        populate_checklist()

        apply_button.config(state = "normal", command = lambda: apply_settings(g_data_logger, date_index, time_index))
        search_button.config(state = "normal", command = lambda: search_for_regex(search_entry.get()))
        search_entry.bind("<Return>", lambda _: search_for_regex(search_entry.get()))
    else:
        info_label = tk.Label(info_frame, text = "File not selected")
        info_label.pack(side = "left")

browse_button.config(command = open_csv_file)

root.protocol("WM_DELETE_WINDOW", _on_close)

root.mainloop()
