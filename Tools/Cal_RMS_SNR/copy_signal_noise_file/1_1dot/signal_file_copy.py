# !usr/bin/env/python
# -*- coding: utf-8 -*-
"""
# version: 1.0
# author : gxq
# file   : signal_file_copy.py
# time   : 2020/8/6 10:02
"""
import os
import shutil

current_path = os.getcwd()
print(current_path)
dest_signal_path = current_path + '/' + 'SNR计算需要数据'
soure_signal_path = current_path + '/' + 'signal'

if not os.path.exists(dest_signal_path):
    os.makedirs(dest_signal_path)


def copy_signal_file(soure_path, target_path):
    files = os.listdir(soure_path)
    for file in files:
        if 'SNR_RMS_EachNode' in file:
            s_path = soure_path + '/' + file
            shutil.copy(s_path, target_path)


def copy_noise_file(soure_path, target_path):
    files = os.listdir(soure_path)
    for file in files:
        if file.lower() == 'noise.txt':
            # print(file)
            s_path = soure_path + '/' + file.lower().capitalize()
            shutil.copy(s_path, target_path)


copy_signal_file(soure_signal_path, dest_signal_path)
copy_noise_file(current_path, dest_signal_path)
