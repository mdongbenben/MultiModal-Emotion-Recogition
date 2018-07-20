#!/usr/bin/python3
import cv2

## opening videocapture
cap = cv2.VideoCapture(0)

## some videowriter props
sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(sz)

fps = 25
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# fourcc = cv2.VideoWriter_fourcc('m', 'p', 'e', 'g')
# fourcc = cv2.VideoWriter_fourcc(*'mpeg')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')


# fourcc = cv2.VideoWriter_fourcc(*'mpeg')

def video_capture(StorePath, video_name):
    ## open and set props
    vout = cv2.VideoWriter(StorePath + video_name, fourcc, fps, sz, True)

    cnt = 0
    while cnt < 250:
        cnt += 1
        time = int(cnt / 25)
        print(cnt)
        _, frame = cap.read()
        cv2.putText(frame, str(time), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)  # 每一帧左上角的绿色数字
        vout.write(frame)

    vout.release()
    cap.release()

# import numpy as np
# import cv2
# import os
#
# np.random.seed(0)
#
# # test different containers
# for fn_mask in ['test_%s.mkv', 'test_%s.avi', 'test_%s.wmv']:
#   # test different codecs
#   for fourcc_name, fourcc in [('uncompressed', 0), ('mp4v', cv2.VideoWriter_fourcc(*'mp4v')), ('xvid', cv2.VideoWriter_fourcc(*'MJPG'))]:
#     fn = fn_mask % fourcc_name
#
#     writer = cv2.VideoWriter(fn, fourcc, 25, (100, 100))
#
#     # generate random 100x100 images
#     for i in range(0,100):
#         img = np.random.random_integers(0, 255, (100,100,3)).astype(np.uint8)
#         writer.write(img)
#
#     writer.release()
#
#     # test result (is generated file too small?)
#     fs = os.path.getsize(fn)
#
#     print('%s [%dB] [%s]' % (fn, fs, 'FAIL' if fs<10000 else 'OK'))
