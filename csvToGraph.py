import csv
# import Tkinter
from Tkinter import *
import tkFileDialog
import os

root = Tk()
# root.geometry("350x500")
# root.withdraw()

main_frame = Frame(root)

browse_frame = Frame(main_frame)
# browse_frame.pack(side = LEFT, expand = "no")

header_frame = Frame(main_frame)
# header_frame.pack(side = LEFT)

for frame in [main_frame, browse_frame, header_frame]:
	frame.pack(expand = True, fill = 'both', side = LEFT)

def open_csv_file():
	file_name = tkFileDialog.askopenfilename(initialdir = root, title = "Select CSV file", filetypes = (("CSV files", "*.csv"),("all files", "*.*")))
	# print(file_name)
	header_frame_set_flag = 0

	if file_name:
		header_array = []
		row_number = 0
		col_number = 0
		num_of_rows = 0

		with open(file_name) as csv_file:
			data_logger = csv.reader(csv_file, delimiter=',')
			col_number = len(next(data_logger))
			# print("number of columns:")
			# print(col_number)
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
					#print(", ".join(row))
					row_number += 1
			
			# print("number of rows:")
			# print(row_number)
			num_of_rows = row_number
			row_number = 0
			csv_file.seek(0)

		# print("header_array len:")
		# print(len(header_array))

		# if header_frame_set_flag == 1:
		#	clear header_frame
		# 	header_frame_set_flag = 0
		# else:
		# 	pass
		
		number_row = 0
		number_column = -1
		for i in range(0, len(header_array), 1):
			header_array[i] = header_array[i][2:-2]			
			if i % 20 == 0:
				number_row = 0
				number_column += 1
			Checkbutton(header_frame, text = header_array[i]).grid(row = number_row, column = number_column)
			number_row += 1
		header_frame_set_flag = 1
		# print("header_array:")
		# print('\n'.join(str(p) for p in header_array))
	else:
		# if header_frame_set_flag == 1:
		# 	# clear header_frame
		# else:
		# 	header_frame_set_flag = 1

		Label(header_frame, text = "File not selected").pack(side = LEFT)
		# print("File not selected")

browse_button = Button(browse_frame, text = "Browse", command = open_csv_file)
# browse_button.pack_propagate(0)
browse_button.pack(side = LEFT)

root.mainloop()

# inp = raw_input()
