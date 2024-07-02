import zmq
import struct
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
socket = context.socket(zmq.SUB)

if( MODE == "ipc"):
    socket.connect("ipc:///tmp/pushpull.ipc")
elif( MODE == "tcp"):
    socket.connect("tcp://localhost:5555")
else:
    print("MODE Error")

# 订阅感兴趣的主题
socket.setsockopt(zmq.SUBSCRIBE, b"latency_test")

while True:
    topic, message = socket.recv_multipart()
    now_time = struct.unpack("d",message)[0]
    latency_list.append(time.time()-now_time)
    # print(f"Received message on topic {topic}: {time}")
