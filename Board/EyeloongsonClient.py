import socket
import sys
import threading
import Contrl
import cv2
import numpy
import time

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定本机地址:
udp_socket.bind(('192.168.137.254', 8888))


def Recivnum():
    receive, client = udp_socket.recvfrom(1024)

    if len(receive):
        print(str(receive, encoding='utf-8'))  # 打印接收的内容
        Contrl.Shakehands()


def SocketIP():
    # 建立sock连接
    # address要连接的服务器IP地址和端口号
    address = ('192.168.137.29', 9999)
    try:
        # 建立socket对象，参数意义见https://blog.csdn.net/rebelqsp/article/details/22109925
        # socket.AF_INET：服务器之间网络通信
        # socket.SOCK_STREAM：流式socket , for TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 开启连接
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    return sock


def SendVideo(sock):
    # 建立图像读取对象
    capture = cv2.VideoCapture(0)
    # 读取一帧图像，读取成功:ret=1 frame=读取到的一帧图像；读取失败:ret=0
    ret, frame = capture.read()
    # 压缩参数，后面cv2.imencode将会用到，对于jpeg来说，15代表图像质量，越高代表图像质量越好为 0-100，默认95
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

    while ret:
        # 停止0.1S 防止发送过快服务的处理不过来，如果服务端的处理很多，那么应该加大这个值
        time.sleep(0.01)
        # cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输
        # '.jpg'表示将图片按照jpg格式编码。
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        # 建立矩阵
        data = numpy.array(imgencode)
        # 将numpy矩阵转换成字符形式，以便在网络中传输
        stringData = data.tobytes()

        # 先发送要发送的数据的长度
        # ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
        sock.send(str.encode(str(len(stringData)).ljust(16)))
        # 发送数据
        sock.send(stringData)
        # 读取服务器返回值
        # 读取下一帧图片
        ret, frame = capture.read()
        cv2.imshow('Client1', frame)

        def recvall(sock, count):
            buf = b''  # buf是一个byte类型
            while count:
                # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
                newbuf = sock.recv(count)
                if not newbuf: return None
                buf += newbuf
                count -= len(newbuf)
            return buf

        length = recvall(sock, 16)  # 获得图片文件的长度,16代表获取长度
        stringData2 = recvall(sock, int(length))  # 根据获得的文件长度，获取图片文件
        data2 = numpy.frombuffer(stringData2, numpy.uint8)  # 将获取到的字符流数据转换成1维数组
        decimg = cv2.imdecode(data2, cv2.IMREAD_COLOR)  # 将数组解码成图像
        cv2.imshow('Clientfrom2', decimg)  # 显示图像

        if cv2.waitKey(10) == 27:
            break

    sock.close()


def Eye():
    sock = SocketIP()
    client_thread = threading.Thread(target=SendVideo, args=(sock,))
    rec_thread = threading.Thread(target=Recivnum)
    client_thread.start()
    rec_thread.start()
    client_thread.join()
    rec_thread.join()
