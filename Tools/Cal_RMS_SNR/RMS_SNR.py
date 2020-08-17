# !usr/bin/env/python
# -*- coding: utf-8 -*-
"""
# version: 1.0
# author : gxq
# file   : RMS_SNR.py
# time   : 2020/8/5 22:35
"""
import os
import math
import pandas as pd
import xlwt
import re

SOFT_VERSION = 'V1.0'
TX_NUM = 0
RX_NUM = 0
NODE_NUM = 0
NODE_LIST = [[2, 3], [9, 3], [15, 3], [2, 18], [9, 18], [15, 18], [2, 35], [9, 35], [15, 35]]
# NODE_LIST = [[2, 3], [8, 3], [15, 3], [2, 18], [8, 18], [15, 18], [2, 35], [9, 35], [15, 35]]

current_path = os.getcwd()
signal_path = current_path
noise_path = current_path + '/' + 'Noise.txt'


def get_chanel_msg():
    tx_num = 0
    rx_num = 0
    with open(noise_path, 'r') as f:
        content = f.read()
        tx_num = re.findall(r'TxNum:(\d{2})', content)[0]
        rx_num = re.findall(r'RxNum:(\d{2})', content)[0]
        # print(tx_num, rx_num)
    return int(tx_num), int(rx_num)


def get_noise_list(path):
    """
    功能：获取需要计算SNR的所有节点Noise
    :param path: noise.txt
    :return:
    """
    mc_noise_list = []
    sc_noise_list = []
    with open(path, 'r') as f:
        content = f.read()
        mc_noise = re.split(r'NoiseAvrSCap', content)[0]
        mc_noise = re.split(r'NoiseMax:\d+\.\d*\n', mc_noise)[1]
        mc_noise = mc_noise.strip()
        mc_noise = mc_noise.split('\n')
        for line in mc_noise:
            line = line.strip()
            line = line.split()
            # print(line)
            mc_noise_list.append(line)
        # print(mc_noise_list)

        sc_noise = re.split(r'NoiseMaxSCapNoProof:\d+\.\d+\n', content)[1]
        sc_noise = sc_noise.strip()
        sc_noise = sc_noise.split('\n')
        # print(sc_noise)
        for line in sc_noise:
            line = line.split()
            sc_noise_list.append(line)
        # print(sc_noise_list)
    return mc_noise_list, sc_noise_list


def get_cal_noise(path):
    mc_noise_list, sc_noise_list = get_noise_list(path)
    mc_need_noise = []
    sc_need_noise = []
    for node in NODE_LIST:
        tx_ch = node[0]
        rx_ch = node[1]
        mc_need_noise.append(float(mc_noise_list[tx_ch-1][rx_ch-1]))
        sc_need_noise.append(float(sc_noise_list[0][rx_ch-1]))

    # print('mc noise:', mc_need_noise)
    # print('sc noise:', sc_need_noise)
    return mc_need_noise, sc_need_noise


def get_one_file_signal(file_path, tx_ch, rx_ch):
    mc_signal_list = []
    sc_signal_list = []
    # print(file_path)
    with open(file_path, 'r') as f:
        content = f.read()
        content = re.split(r'RMS Noise Of Each Node', content)[0]
        content = re.split(r'Signal Of Each Node:', content)[1]
        content = content.strip()
        signal = content.split('\n')
        for i in range(TX_NUM):
            mc_signal_list.append(signal[i].strip().split())

        sc_signal_list.append(signal[TX_NUM+2].strip().split())
        # print(mc_signal_list[tx_ch-1][rx_ch-1])
        # print(sc_signal_list[0][rx_ch-1])

    return mc_signal_list[tx_ch-1][rx_ch-1], sc_signal_list[0][rx_ch-1]


def get_signal(path):
    """
    功能：获取需要计算SNR的所有节点信号量
    :param path:
    :return:
    """
    files = os.listdir(path)
    signal_file_cnt = 0
    node_file_dict = {}
    mc_node_signal_dict = {}
    sc_node_signal_dict = {}
    mc_signal_list = []
    sc_signal_list = []
    for file in files:
        if 'SNR_RMS_EachNode' in file:
            signal_file_cnt += 1
            node_index = file.split('_SNR_RMS_EachNode')[0]
            if node_index not in node_file_dict.keys():
                node_file_dict[node_index] = file

    # print(node_file_dict)
    for file_index, file in node_file_dict.items():
        # print(file_index, file)
        file_path = path + '/' + file
        node_index = int(file_index)
        tx_chanel = NODE_LIST[node_index-1][0]
        rx_chanel = NODE_LIST[node_index-1][1]
        node_mc_signal, node_sc_signal = get_one_file_signal(file_path, tx_chanel, rx_chanel)
        # print(node_mc_signal, node_sc_signal)

        # 统计互容MC的signal
        if node_index not in mc_node_signal_dict.keys():
            mc_node_signal_dict[node_index] = float(node_mc_signal)

        # 统计自容SC的signal
        if node_index not in sc_node_signal_dict.keys():
            sc_node_signal_dict[node_index] = float(node_sc_signal)

    # print(mc_node_signal_dict)
    # print(sc_node_signal_dict)
    print('Need Cal Node Mc Signal is:', end=' ')
    for i in range(1, NODE_NUM+1):
        print(mc_node_signal_dict[i], end=' ')
        mc_signal_list.append(mc_node_signal_dict[i])
    print('')

    print('Need Cal Node Sc Signal is:', end=' ')
    for i in range(1, NODE_NUM+1):
        print(sc_node_signal_dict[i], end=' ')
        sc_signal_list.append(sc_node_signal_dict[i])
    print('')
    # print(mc_signal_list)
    return mc_signal_list, sc_signal_list


def cal_node_snr(signal, noise):
    """
    计算单节点的SNR
    :param signal: 单节点的信号量
    :param noise: 单节点的噪声值
    :return:
    """
    snr_temp = signal/noise
    # print(snr_temp)
    snr = 20*math.log10(snr_temp)
    # print(snr)
    return snr


def cal_snr():
    """
    功能：计算所有需要计算的节点SNR
    :return:
    """


    mc_snr_list = []
    sc_snr_list = []

    mc_cal_node_signal, sc_cal_node_signal = get_signal(signal_path)
    mc_cal_node_noise, sc_cal_node_noise = get_cal_noise(noise_path)

    # 计算互容SNR
    for i in range(NODE_NUM):
        snr = cal_node_snr(mc_cal_node_signal[i], mc_cal_node_noise[i])
        snr = round(snr, 2)
        mc_snr_list.append(snr)

    # 计算自容SNR
    for i in range(NODE_NUM):
        snr = cal_node_snr(sc_cal_node_signal[i], sc_cal_node_noise[i])
        snr = round(snr, 2)
        sc_snr_list.append(snr)

    # for i in range(3):
    #     sc_snr_list[i] = round(sum(sc_snr_list[i:i+3])/3)

    # 需要计算节点的signal、noise、snr保存到文本中
    with open('./SNR计算结果.txt', 'w') as f:
        f.write('Node Mc Signal: '+' '.join(map(str, mc_cal_node_signal))+'\n')
        f.write('Node Mc Noise: ' + ' '.join(map(str, mc_cal_node_noise)) + '\n')
        f.write('Node Mc SNR: ' + ' '.join(map(str, mc_snr_list)) + '\n')

        f.write('Node Sc Signal: '+' '.join(map(str, sc_cal_node_signal))+'\n')
        f.write('Node Sc Noise: ' + ' '.join(map(str, sc_cal_node_noise)) + '\n')
        f.write('Node Sc SNR: ' + ' '.join(map(str, sc_snr_list)) + '\n')

    # 保存到Excel
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('SNR')

    worksheet.write(1, 1, 'Mc Signal')
    for i in range(len(mc_cal_node_signal)):
        worksheet.write(1, 2+i, mc_cal_node_signal[i])

    worksheet.write(2, 1, 'Mc Noise')
    for i in range(len(mc_cal_node_noise)):
        worksheet.write(2, 2+i, mc_cal_node_noise[i])

    worksheet.write(3, 1, 'Mc SNR')
    for i in range(len(mc_snr_list)):
        worksheet.write(3, 2+i, mc_snr_list[i])

    worksheet.write(4, 1, 'Sc Signal')
    for i in range(len(sc_cal_node_signal)):
        worksheet.write(4, 2+i, sc_cal_node_signal[i])

    worksheet.write(5, 1, 'Sc Noise')
    for i in range(len(sc_cal_node_noise)):
        worksheet.write(5, 2+i, sc_cal_node_noise[i])

    worksheet.write(6, 1, 'Sc SNR')
    for i in range(len(sc_snr_list)):
        worksheet.write(6, 2+i, sc_snr_list[i])

    workbook.save('SNR.xls')

    return mc_snr_list, sc_snr_list


TX_NUM, RX_NUM = get_chanel_msg()
NODE_NUM = len(NODE_LIST)
mc_snr_result, sc_snr_result = cal_snr()
print('Mc SNR is:', mc_snr_result)
print('Sc SNR is:', sc_snr_result)
