import csv
from tkinter import *
from tkinter.filedialog import *
import os

root = Tk()

main_frame = Frame(root)

browse_frame = Frame(main_frame)

info_frame = Frame(main_frame)

for frame in [main_frame, browse_frame, info_frame]:
	frame.pack(expand = True, fill = "both", side = "left")

def apply_settings():
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
			col_number = len(next(data_logger))
			csv_file.seek(0)

			for row in data_logger:
				if row_number == 0:
					j = 1
					for i in range(0, col_number, 1):
						if j <= col_number:
							header_array.append(str(row[i:j]))
							j += 1
					row_number += 1
				else:
					row_number += 1
			num_of_rows = row_number
			row_number = 0
			csv_file.seek(0)
		
		number_row = 0
		number_column = -1
		for i in range(0, len(header_array), 1):
			header_array[i] = header_array[i][2:-2]			
			if i % 20 == 0:
				number_row = 0
				number_column += 1
			Checkbutton(header_frame, text = header_array[i]).grid(row = number_row, column = number_column)
			number_row += 1
	else:
		info_label = Label(info_frame, text = "File not selected")
		info_label.pack(side = "left")

browse_button = Button(browse_frame, text = "Browse", command = open_csv_file)
browse_button.pack(side = "left")

root.mainloop()
