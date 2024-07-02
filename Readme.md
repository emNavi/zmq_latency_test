# python ZMQ 机内通讯性能测试

测试采用的方式为：

> 发送方发送当前时间，接收方接收后根据当前时间以及接收到的消息计算延时，即单向通讯延时

测试平台
- Thinkpad x13 gen3 (6800u)
- ubuntu22.04

测试结果如下，其中
- 首次延时描述了，程序构建连接后初次交换数据的时延，在测试中，首次延时每次的变化幅度较大，因此只需明确首次通讯延时较高即可
- 平均延时展示了不同发送频率下的通讯延时。
- sub_pub 是一对多通讯，这里我们仅展示1对1通讯。
- 测试中最少测试1k次，有特殊标注的更高


| 通讯方式 | 通讯模型 | 首次延时 | 平均延时(1khz) | 平均延时(100hz) |
|---------|--------|---------|---------------|---------------|
|tcp| REQ_REP |  1.1~1.4ms | req(0.20ms)rep(0.24ms)(10k_times)| req(0.25ms)rep(0.5ms)|
|tcp| PUSH_PULL | 80ms | 0.3ms(10k_times) | 0.48ms(10k_times)|
|ipc| PUSH_PULL | (23~120)ms | 0.23ms(10k_times) | 0.31~0.37ms|
|tcp| SUB_PUB | 0.45~0.78ms | 0.23ms~0.27ms |0.42ms~0.62ms |
|ipc| SUB_PUB | 0.42~0.87ms | 0.27ms~0.29ms |0.39ms~0.55ms |


# 测试
为了保证第一次延时测试的准确，需要先开接收端

# 通讯模式特性

## PUSH_PULL Mode

**Pusher（推送者）向Puller（拉取者）** 推送消息。Pusher 可以向多个 Puller 推送消息，但每条消息只能被一个 Puller 接收。

Puller 从 Pusher 接收消息。一个 Puller 可以从多个 Pusher 接收消息，但每个消息只能被一个 Puller 接收。

push 和 pull的任意一方