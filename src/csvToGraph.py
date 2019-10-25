import csv
from tkinter import *
from tkinter.filedialog import *
import os

root = Tk()

main_frame = Frame(root)
browse_frame = Frame(main_frame)
info_frame = Frame(main_frame)

checked_dict = {}

for frame in [main_frame, browse_frame, info_frame]:
    frame.pack(expand = True, fill = "both", side = "left")

def apply_settings():
    for (key, value) in checked_dict.items():
        if value.get() == 1:
            print(key)
            print(value.get())
    dir_name = askdirectory()
    print(dir_name)

def open_csv_file():
    for widget in info_frame.winfo_children():
        widget.destroy()

    file_name = askopenfilename(initialdir = root, title = "Select CSV file", filetypes = (("CSV files", "*.csv"),("all files", "*.*")))

    if file_name:
        header_array = []
        row_number = 0
        col_number = 0
        num_of_rows = 0

        header_window = Toplevel(root)
        header_frame = Frame(header_window)
        apply_frame = Frame(header_window)
        for frame in [header_frame, apply_frame]:
            frame.pack(expand = True, fill = "both", side = "left")

        apply_button = Button(apply_frame, text = "Apply", command = apply_settings)
        apply_button.pack(side = "bottom")

        with open(file_name) as csv_file:
            data_logger = csv.reader(csv_file, delimiter=",")
            col_number = len(next(data_logger)) - 1
            csv_file.seek(0)

            for row in data_logger:
                if row_number == 0:
                    for element in row:
                        if element:
                            header_array.append(element)
                row_number += 1
            num_of_rows = row_number
            row_number = 0
            csv_file.seek(0)

        number_row = 0
        number_column = 0
        for item in header_array:
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

root.mainloop()
