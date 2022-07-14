import socket
import threading
import time
import cv2
import numpy


# 创建服务端的socket对象socketserver
socketserver = socket.socket(
    socket.AF_INET,  # AF_INET 表示服务器到服务器通信
    socket.SOCK_STREAM  # SOCK_STREAM 表示 socket 连接
)
host = '192.168.43.49'
port = 9999
# 绑定地址（包括ip地址会端口号）
socketserver.bind((host, port))
# 设置监听
socketserver.listen(5)
i = 0

Coonlist = [None] * 2

Addrlist = [None] * 2


def Sentdata(num, ip):
    dest = (ip, 8888)
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Data_encode = bytes(str(int(num)), encoding='utf-8')
        udp_socket.sendto(Data_encode, dest)
    except Exception:
        print("失败\n")


def recvall(sock, count):
    buf = b''  # buf是一个byte类型
    while count:
        # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def handle_sock(conn, addr):
    print('connect from:' + str(addr))
    while 1:
        length = recvall(conn, 16)  # 获得图片文件的长度,16代表获取长度
        stringData = recvall(conn, int(length))  # 根据获得的文件长度，获取图片文件
        data = numpy.frombuffer(stringData, numpy.uint8)  # 将获取到的字符流数据转换成1维数组
        decimg = cv2.imdecode(data, cv2.IMREAD_COLOR)
        try:
            if conn == Coonlist[0]:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

                result, imgencode2 = cv2.imencode('.jpg', decimg, encode_param)

                data2 = numpy.array(imgencode2)
                # 将numpy矩阵转换成字符形式，以便在网络中传输
                stringData2 = data2.tobytes()
                if Coonlist[1] is None:
                    pass
                else:
                    Coonlist[1].send(str.encode(str(len(stringData2)).ljust(16)))
                    Coonlist[1].send(stringData2)
                    Sentdata(1, addr[0])
            else:
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

                result, imgencode2 = cv2.imencode('.jpg', decimg, encode_param)

                data2 = numpy.array(imgencode2)
                # 将numpy矩阵转换成字符形式，以便在网络中传输
                stringData2 = data2.tobytes()
                if Coonlist[0] is None:
                    pass
                else:
                    Coonlist[0].send(str.encode(str(len(stringData2)).ljust(16)))
                    Coonlist[0].send(stringData2)
                    Sentdata(1, addr[0])

        except Exception:
            print("对方不在线\n")
            continue
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break


def ReceiveVideo():
    global i
    while 1:
        # 等待客户端的连接
        # 注意：accept()函数会返回一个元组
        # 元素1为客户端的socket对象，元素2为客户端的地址(ip地址，端口号)
        clientsocket, addr = socketserver.accept()
        print(clientsocket)
        print(Coonlist)
        Coonlist[i] = clientsocket
        Addrlist[i] = addr
        client_thread = threading.Thread(target=handle_sock, args=(clientsocket, addr))
        client_thread.start()
        i += 1


if __name__ == '__main__':
    ReceiveVideo()    #  眉目传情

