import socket
import time
import cv2
import numpy
import Pushup
import Pullup
import Situp
import Squat


def ReceiveVideo():
    # IP地址'0.0.0.0'为等待客户端连接
    address = ('0.0.0.0', 8888)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 将套接字绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址.
    s.bind(address)
    # 开始监听TCP传入连接。参数指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。
    s.listen(1)

    def recvall(sock, count):
        buf = b''  # buf是一个byte类型
        while count:
            # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    conn, addr = s.accept()
    print('connect from:' + str(addr))
    while 1:
        start = time.time()  # 用于计算帧率信息
        length = recvall(conn, 16)  # 获得图片文件的长度,16代表获取长度
        stringData = recvall(conn, int(length))  # 根据获得的文件长度，获取图片文件
        data = numpy.frombuffer(stringData, numpy.uint8)  # 将获取到的字符流数据转换成1维数组
        decimg = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 将数组解码成图像
        # facetime.PoseMain(decimg)
        # Pushup.pushup(decimg)
        # Pullup.pullup(decimg)
        # Situp.situp(decimg)
        Squat.squat(decimg)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
    s.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    ReceiveVideo()
