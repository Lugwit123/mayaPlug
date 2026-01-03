import socket

# 创建socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口号
s.bind(('192.168.1.27', 8888))

# 开始监听
s.listen()

# 接受连接
conn, addr = s.accept()
print(f"Connected by {addr}")

# 发送消息
conn.sendall(b"dasasdasXXdsdX")

# 关闭连接
conn.close()

