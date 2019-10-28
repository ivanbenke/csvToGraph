import csv
from tkinter import *
from tkinter import filedialog as fd
from matplotlib import pyplot as plt
from copy import deepcopy
from sys import platform
import os

def _configure_frame_scrolling(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def _mouse_wheel_handler(event):
    if sys.platform.startswith("linux") or sys.platform.startswith("win32"):
        scroll_count = int(-1*(event.delta/120))
    elif sys.platform.startswith("darwin"):
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

root = Tk()

main_frame = Frame(root, width="500", height="800")
main_frame.pack(expand = True, fill = "both", side = "left")
main_frame.pack_propagate(0)

search_frame = Frame(main_frame)
search_frame.pack(expand = True, fill = "x", side = "top")
# search_frame.pack_propagate(0)
search_label = Entry(search_frame)
search_label.pack(expand = True, fill = "x", side = "top")

main_header_frame = Frame(main_frame, width="480", height="700")
main_header_frame.pack(expand = True, fill = "both", side = "top")
main_header_frame.pack_propagate(0)

header_canvas = Canvas(main_header_frame)
header_frame = Frame(header_canvas)
vertical_sb = Scrollbar(main_header_frame, orient="vertical", command=header_canvas.yview)

header_canvas.configure(yscrollcommand=vertical_sb.set)

vertical_sb.pack(fill="y", side="right")

header_canvas.pack(expand = True, fill = "y", side = "left")
# header_canvas.pack_propagate(0)
header_canvas.create_window((4,4), window=header_frame, anchor="nw")

header_frame.bind("<Configure>", lambda event, canvas=header_canvas: _configure_frame_scrolling(header_canvas))

header_frame.bind("<Enter>", _bound_to_mousewheel)
header_frame.bind("<Leave>", _unbound_to_mousewheel)

# # Windows/Mac
# header_canvas.bind_all("<MouseWheel>", _mouse_wheel_handler)
# # Linux
# header_canvas.bind_all("<Button-4>", _mouse_wheel_handler)
# header_canvas.bind_all("<Button-5>", _mouse_wheel_handler)

# header_frame.pack(expand = True, fill = "y", side = "top")
# header_frame.pack_propagate(0)

browse_frame = Frame(main_frame)
browse_frame.pack(expand = True, fill = "x", side = "bottom")
# browse_frame.pack_propagate(0)

info_frame = Frame(main_frame)
info_frame.pack(expand = True, fill = "x", side = "bottom")
# info_frame.pack_propagate(0)

apply_frame = Frame(main_frame)
apply_frame.pack(expand = True, fill = "x", side = "right")
# apply_frame.pack_propagate(0)

header_array = []
checked_dict = {}

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
            plt.savefig(graph_filename)
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

        # header_window = Toplevel(root)
        # header_frame = Frame(header_window)
        # apply_frame = Frame(header_window)
        # for frame in [header_frame, apply_frame]:
        #     frame.pack(expand = True, fill = "both", side = "left")

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
                # if number_row == 20:
                #     number_row = 0
                #     number_column += 1
                Checkbutton(header_frame, text = item, variable = checked_var).grid(row = number_row, column = number_column)
                checked_dict.update({item:checked_var})
                number_row += 1
    else:
        info_label = Label(info_frame, text = "File not selected")
        info_label.pack(side = "left")

browse_button = Button(browse_frame, text = "Browse", command = open_csv_file)
browse_button.pack(side = "left")

def on_close():
    plt.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
