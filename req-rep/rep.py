# rep_server.py

import zmq
import time
import signal
import sys
import statistics

###############setting
MODE = "udp"
# ipc tcp udp
############### 

latency_list = []
def show(sig, frame):
    global latency_list
    print("首次延时",latency_list[0])
    latency_list = latency_list[1:]

    # 计算平均值
    average = statistics.mean(latency_list)

    # 计算最大值
    maximum = max(latency_list)

    # 计算最小值
    minimum = min(latency_list)

    # 计算方差
    variance = statistics.variance(latency_list)

    print("平均值:", average)
    print("最大值:", maximum)
    print("最小值:", minimum)
    print("方差:", variance)
    # 执行其他必要的清理操作
    sys.exit(0)

signal.signal(signal.SIGINT, show)

context = zmq.Context()

# REP端
socket_rep = context.socket(zmq.REP)
socket_rep.bind("tcp://*:5555")

# 接收请求并回复
while True:
    message = socket_rep.recv_string()
    latency = time.time() - float(message)
    latency_list.append(latency)    

     
    # 回复消息
    currtent_time = time.time()
    socket_rep.send_string(str(currtent_time))
# 关闭套接字
socket_rep.close()
context.term()
