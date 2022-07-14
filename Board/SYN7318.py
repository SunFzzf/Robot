# encoding=utf-8
from time import sleep
import serial
import EyeloongsonClient
import SportLoongsonSent
import PoseLoongsonSent
import Det

def Speak(str):
    str_gbk=str.encode('gbk')
    data_len=len(str_gbk)+2
    len_hex='{:02X}'.format(data_len)
    data_send=b'\xfd'+b'\x00'+bytes.fromhex(len_hex)+b'\x01\x01'+str_gbk
    com.write(data_send)
    for i in range(8):
        com.read()
    sleep(0.2*data_len)

def Listen():
    while(True):
        data_state=b'\xFD\x00\x01\x21'
        com.write(data_state)
        for i in range(8):
            modstate=com.read()
        
        if(modstate==b'\x4F'):
            data_send=b'\xFD\x00\x02\x10\x03'
            com.write(data_send)
            for i in range(4):
                com.read()
            print("开始识别")
            com.read()
            com.read()
            recvdata_len=com.read()
            if(recvdata_len==b'\x01'):
                com.read()
            else:
                for i in range(4):
                    recvid=com.read()
                if(recvid==b'\x00'):
                    Speak("我在")
                elif(recvid==b'\x01'):
                    Speak("关怀模式已启动")
                elif(recvid==b'\x02'):
                    Speak("运动模式已启动")
                    SportLoongsonSent.Sport()
                elif(recvid==b'\x03'):
                    Speak("跌倒检测已启动")
                elif(recvid==b'\x04'):
                    Speak("入侵检测已启动")
                    Det.Det()
                elif(recvid==b'\x05'):
                    Speak("工作助手已启动")
                    PoseLoongsonSent.Pose()
                elif(recvid==b'\x06'):
                    Speak("灵犀系统已启动")
                    EyeloongsonClient.Eye()

if __name__ == '__main__':    
    com = serial.Serial('/dev/ttyS1', 115200)
    word=b'\xFD\x00\x3F\x1F\x01\x33\xBD\xF0\xC9\xC1\xC9\xC1\x7C\xB9\xD8\xBB\xB3\xC4\xA3\xCA\xBD\x7C\xD4\xCB\xB6\xAF\xC4\xA3\xCA\xBD\x7C\xB5\xF8\xB5\xB9\xBC\xEC\xB2\xE2\x7C\xC8\xEB\xC7\xD6\xBC\xEC\xB2\xE2\x7C\xB9\xA4\xD7\xF7\xD6\xFA\xCA\xD6\x7C\xC1\xE9\xCF\xAC\xCF\xB5\xCD\xB3'
    com.write(word)
    for i in range(8):
        com.read()
    Listen()
