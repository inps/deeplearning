# -*- coding: utf-8 -*-
import face_recognition  
import cv2  
import os
import subprocess
import numpy as np
import logging
#import ffmpeg


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 这是网络摄像头上实时运行人脸识别
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# 请注意：这个例子需要安装OpenCV
# 具体的演示。如果你安装它有困难，试试其他不需要它的演示。
# 得到一个参考的摄像头# 0（默认）
# 本地摄像头
#video_capture = cv2.VideoCapture(0)
# 网络摄像头
#video_capture = cv2.VideoCapture("rtsp://admin:1qazxsw2@10.192.42.143:554/main/Channels/1")
video_capture = cv2.VideoCapture("rtsp://admin:1qazxsw2@10.192.42.143:554/Streaming/Channels/102")
# 加载示例图片并学习如何识别它。
#在同级目录下的images文件中放需要被识别出的人物图
#path ="/data/face/pic"
path ="E:/soft/apic"
total_image=[]
total_image_name=[]
total_face_encoding=[]
for fn in os.listdir(path): #fn 表示的是文件名
  total_face_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+fn))[0])
  fn=fn[:(len(fn)-4)]#截取图片名（这里应该把images文件中的图片名命名为为人物名）
  total_image_name.append(fn)#图片名字列表


# 视频属性
rtmpUrl = 'rtmp://127.0.0.1:1935/live/stream'
size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
sizeStr = str(size[0]) + 'x' + str(size[1])
fps = video_capture.get(cv2.CAP_PROP_FPS) 

#ffmpeg -rtsp_transport tcp -i "rtsp://admin:kiatnys1@10.192.42.143:554/Streaming/Channels/102" -vcodec copy -acodec copy -f flv "rtmp://127.0.0.1:1935/live/stream"
#ffplay “rtmp://127.0.0.1:1935/live/stream“  >>  直接播放  
#http://127.0.0.1:8080   >>   RTMP 监控 >> rtmp://127.0.0.1:1935/live/stream
#                                       RTMP 点播测试器 >> rtmp://127.0.0.1:1935/live/stream




command = ['ffmpeg',
    '-y',
 #   '-re',
 #   '-rtsp_transport', 'tcp',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', sizeStr,
    '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv', 
    rtmpUrl]

# print("xx:",command)

# pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
pipe = subprocess.Popen(command, stdin=subprocess.PIPE)#,shell=False)
#pipe = os.popen(command, stdin=subprocess.PIPE,shell=True)
out_filename = 'rtmp://127.0.0.1:1935/live/stream'
width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height  = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


# process2 = start_ffmpeg_process2(out_filename, width, height)

# def write_frame(process2, frame):
#     logger.debug('Writing frame')
#     process2.stdin.write(
#         frame
#         .astype(np.uint8)
#         .tobytes()
#     )
# def start_ffmpeg_process2(out_filename, width, height):
#     logger.info('Starting ffmpeg process2')
#     args = (
#         ffmpeg
#         .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
#         .output(out_filename, pix_fmt='yuv420p')
#         .overwrite_output()
#         .compile()
#     )
#     return subprocess.Popen(args, stdin=subprocess.PIPE)

# args = (
#         ffmpeg
#         .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
#         .output(out_filename, pix_fmt='yuv420p')
#         .overwrite_output()
#         .compile()
#     )
# process2 = subprocess.Popen(args, stdin=subprocess.PIPE)


while True:
  # 抓取一帧视频
  ret, frame = video_capture.read()
  # 发现在视频帧所有的脸和face_enqcodings
  face_locations = face_recognition.face_locations(frame)
  face_encodings = face_recognition.face_encodings(frame, face_locations)
  # 在这个视频帧中循环遍历每个人脸
  for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      # 看看面部是否与已知人脸相匹配。
      for i,v in enumerate(total_face_encoding):
          match = face_recognition.compare_faces([v], face_encoding,tolerance=0.5)
          name = "Unknown"
          if match[0]:
              name = total_image_name[i]
              break
      # 画出一个框，框住脸
      cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
      # 画出一个带名字的标签，放在框下
      cv2.rectangle(frame, (left, bottom - 10), (right, bottom), (0, 0, 255), cv2.FILLED)
      font = cv2.FONT_HERSHEY_DUPLEX
      cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
  
      #通过ffmpeg输出到远程rtmp服务器
  pipe.stdin.write(frame.astype(np.uint8).tobytes())
#   process2.stdin.write(
#         frame
#         .astype(np.uint8)
#         .tobytes()
#     )
  # 显示结果图像
  #cv2.imshow('Video', frame)
  # 按q退出
  #if cv2.waitKey(1) & 0xFF == ord('q'):
  #    break
# 释放摄像头中的流
video_capture.release()
cv2.destroyAllWindows()

