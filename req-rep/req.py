import zmq
import time
import signal
import sys
import statistics

###############setting
MODE = "udp"
time_gap = 0.01
loop_times = 1000
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

# REQ端
socket_req = context.socket(zmq.REQ)
socket_req.connect("tcp://localhost:5555")

# 发送消息
for i in range(loop_times):
    current_time = time.time()
    socket_req.send_string(str(current_time))

    # 接收回复
    message = socket_req.recv_string()
    latency = time.time() -float(message)
    latency_list.append(latency)    
    time.sleep(time_gap)

# 关闭套接字
socket_req.close()
context.term()
show(1,2)
