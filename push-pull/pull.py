import zmq
import time
import signal
import sys
import statistics

###############setting
MODE = "ipc"
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

# 创建一个 PULL 套接字
socket = context.socket(zmq.PULL)
if( MODE == "ipc"):
    socket.connect("ipc:///tmp/pushpull.ipc")
elif( MODE == "tcp"):
    socket.connect("tcp://localhost:5555")
else:
    print("MODE Error")
    
# 接收请求并回复
while True:
    message = socket.recv_string()
    latency = time.time() - float(message)
    latency_list.append(latency)
    # print("latency", latency)
print(latency_list)
# 关闭套接字
socket.close()
context.term()
