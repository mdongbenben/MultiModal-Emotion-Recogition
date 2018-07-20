import subprocess
import requests
import os
import cv2
import time
from video_capture import video_capture


# basepath = 'C:\\Project\\base\\SentimentAnalysis\\Emotion-Audio\\Raw_Data\\AudioVisualClip\\JK\\'

def video2audio_convert(video, audio):
    command = "C:\\ffmpeg\\bin\\ffmpeg -i" + " " + video + " " + "-ab 160k -ac 1 -ar 44100 -vn" + " " + audio
    subprocess.call(command, shell=True)


def checkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    outAudioPath = 'C:\\Project\\base\\SentimentAnalysis\\Emotion\\OutAudio\\'
    outVideoPath = 'C:\\Project\\base\\SentimentAnalysis\\Emotion\\OutVideo\\'
    checkPath(outAudioPath)
    checkPath(outVideoPath)

    capture_video = 'test.avi'
    video_capture(outVideoPath, capture_video)
    video_name = capture_video.split('.')[0]
    audio = outAudioPath + video_name + '_out.wav'
    print(audio)
    video = outVideoPath + video_name + '.avi'
    print(video)
    video2audio_convert(video, audio)
    if os.path.exists(audio):
        print('convert success')
    url = 'http://127.0.0.1:5000/audio_emotion_classify'
    # emotion = requests.put(url, data={'data': audio})
    # print(emotion.json())

    # # 指定文件夹所有视频的音频提取
    # i = 0
    # for file in files:
    #     video_name = file.split('.')[0]
    #     outAudioPath = outpath + video_name + '_out.wav'
    #     inputVideoPath = basepath + video_name + '.avi'
    #     if not os.path.exists(outAudioPath):
    #         video2audio_convert(inputVideoPath, outAudioPath)
    #         print('convert success')
    #     url = 'http://127.0.0.1:5000/audio_emotion_classify'
    #     emotion = requests.put(url, data={'data': outAudioPath})
    #     print(emotion.json(), i)
    #     i = i + 1
