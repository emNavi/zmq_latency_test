# req_client.py

import zmq
import time
import struct

########### setting
loop_times = 1000
time_gap = 0.01
MODE = "ipc"
# ipc tcp
############
context = zmq.Context()

socket = context.socket(zmq.PUB)
if( MODE == "ipc"):
    socket.bind("ipc:///tmp/pushpull.ipc")
elif( MODE == "tcp"):
    socket.bind("tcp://localhost:5555")
else:
    print("MODE Error")
# 发送消息
topic = b"latency_test"  # 定义主题，需使用字节串
for i in range(loop_times):
    current_time = time.time()
    socket.send_multipart([topic,  struct.pack('d', current_time)])
    pack_time = struct.pack('d', current_time)
    time.sleep(time_gap)
print("PUSH 完成，请退出sub程序")

# 关闭套接字
socket.close()
context.term()

