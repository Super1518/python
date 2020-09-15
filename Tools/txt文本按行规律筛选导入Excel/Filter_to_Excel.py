# !usr/bin/env/python
# -*- coding: utf-8 -*-
"""
# version: 1.0
# author : guoxunqiang 
# file   : sepratator.py
# time   : 2020/9/15 22:14
"""
import xlwt
import os

file_path = 'data.txt'
xls_path = 'data.xls'

col_start = 2  # Excel第3行
row_start = 4  # Excel第4列

# 创建工作簿
def create_book():
    book = xlwt.Workbook()
    return book


# 创建工作表
def create_sheet(book_name, sheet_name):
    sheet = book_name.add_sheet(sheet_name, cell_overwrite_ok=True)
    return sheet


# 保存工作簿
def save_book(book_name, save_file_name):
    book_name.save(save_file_name)


# 向某一个单元格写入指定的数据
def write_cell_data(sheet, col, row, data):
    sheet.write(col, row, data)


# 向一行的多个单元格写入数据
def write_line_data(sheet, col_start, row_start, row_nums, data_list):
    if len(data_list) == 0 or row_nums > len(data_list):
        return None

    data_idx = 0
    for each_row in range(row_nums):
        write_cell_data(sheet, col_start, (row_start+each_row), int(data_list[data_idx]))
        data_idx += 1


mybook = create_book()  # 创建工作簿
mysheet = create_sheet(mybook, 'data')  # 创建data工作表
write_cell_data(mysheet, 2, 1, "differ")
write_cell_data(mysheet, 2, 2, "X坐标")
write_cell_data(mysheet, 2, 3, "Y坐标")

with open(file_path, 'r') as f:
    line = f.readline()
    read_start_flag = False
    read_line_cnt = 0
    poit_num = 0
    col_cnt = col_start
    while line:
        line = line.strip()
        line_list = line.split()
        list_len = len(line_list)

        if list_len == 10:
            row_start = 4
            read_start_flag = True
            poit_num = int(line_list[-1])
            read_line_cnt = 8 + poit_num
            col_cnt += 1  # 空一行写入
            write_line_data(mysheet, col_cnt, row_start, list_len, line_list)
            # col_cnt += 1
            line = f.readline()
            continue

        if read_line_cnt > 0:
            if poit_num > 0:
                row_start = 1
                poit_num -= 1
                # col_cnt -= 1
            else:
                row_start = 4

            print(line_list)
            read_line_cnt -= 1
            write_line_data(mysheet, col_cnt, row_start, list_len, line_list)
            col_cnt += 1

        # if read_start_flag == True:
        #     read_start_flag = False
        line = f.readline()

save_book(mybook, xls_path)  # 保存工作簿




