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


TX_NUM = 16
RX_NUM = 36

NODE_NUM = 9
NODE_LIST = [[2, 3], [9, 3], [15, 3], [2, 18], [9, 18], [15, 18], [2, 35], [9, 35], [15, 35]]

current_path = os.getcwd()

signal_path = current_path
noise_path = current_path + '/' + 'Noise.txt'


def get_noise(path):
    """
    功能：获取需要计算SNR的所有节点Noise
    :param path: noise.txt
    :return:
    """
    mc_need_cal_node_noise = []
    sc_need_cal_node_noise = []
    mc_noise_data_start_line = 8
    # mc_noise_data_end_line = mc_noise_data_start_line + TX_NUM
    with open(path, 'r') as f:
        lines = f.readlines()
        # print(lines)
        tx_chanel = 0
        rx_chanel = 0
        for i in range(0, NODE_NUM):
            tx_chanel = NODE_LIST[i][0]
            rx_chanel = NODE_LIST[i][1]
            # print('tx = %d rx = %d' % (tx_chanel, rx_chanel))
            line_noise = lines[mc_noise_data_start_line+tx_chanel-1]
            line_noise = line_noise.strip()
            line_noise = line_noise.split()
            # print(line_noise)
            node_noise = line_noise[rx_chanel-1]
            # print(node_noise)
            mc_need_cal_node_noise.append(float(node_noise))

        print('Need Cal Node Mc Noise is :', end=' ')
        for i in range(len(mc_need_cal_node_noise)):
            print(mc_need_cal_node_noise[i], end=' ')
        print(end='\n')

        # 统计自容SC的noise数据
        sc_noise_data_start_line = 41
        for i in range(0, NODE_NUM):
            tx_chanel = NODE_LIST[i][0]
            rx_chanel = NODE_LIST[i][1]
            # print('tx = %d rx = %d' % (tx_chanel, rx_chanel))
            line_noise = lines[sc_noise_data_start_line - 1]
            line_noise = line_noise.strip()
            line_noise = line_noise.split()
            node_noise = line_noise[rx_chanel - 1]
            sc_need_cal_node_noise.append(float(node_noise))

        print('Need Cal Node Sc Noise is :', end=' ')
        for i in range(len(sc_need_cal_node_noise)):
            print(sc_need_cal_node_noise[i], end=' ')
        print(end='\n')
    return mc_need_cal_node_noise, sc_need_cal_node_noise


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
        mc_signal_start_line = 6
        sc_signal_start_line = mc_signal_start_line + TX_NUM + 3
        node_index = int(file_index)
        tx_chanel = NODE_LIST[node_index-1][0]
        rx_chanel = NODE_LIST[node_index-1][1]

        with open(file_path, 'r') as f:
            lines = f.readlines()

            # 统计互容MC的signal
            mc_line_signal = lines[mc_signal_start_line + tx_chanel - 1]
            mc_line_signal = mc_line_signal.strip().split()
            node_signal = mc_line_signal[rx_chanel-1]
            # print(node_signal)
            if node_index not in mc_node_signal_dict.keys():
                mc_node_signal_dict[node_index] = float(node_signal)

            # 统计自容SC的signal
            sc_line_signal = lines[sc_signal_start_line - 1]
            sc_line_signal = sc_line_signal.strip().split()
            node_signal = sc_line_signal[rx_chanel-1]
            # print(node_signal)
            if node_index not in sc_node_signal_dict.keys():
                sc_node_signal_dict[node_index] = float(node_signal)


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
    mc_cal_node_noise, sc_cal_node_noise = get_noise(noise_path)
    mc_cal_node_signal, sc_cal_node_signal = get_signal(signal_path)
    # print(len(cal_node_signal))
    # print(len(cal_node_noise))

    mc_snr_list = []
    sc_snr_list = []
    if len(mc_cal_node_noise) != NODE_NUM or len(mc_cal_node_noise) != NODE_NUM:
        print('signal len != noise len, please check!')
        return mc_snr_list

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
    return mc_snr_list, sc_snr_list


mc_snr_result, sc_snr_result = cal_snr()
print('Mc SNR is:', mc_snr_result)
print('Sc SNR is:', sc_snr_result)
