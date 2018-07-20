from flask import Flask,request
from flask_restful import reqparse, abort, Api, Resource
import wave
from keras.models import load_model
import calculate_features as cf
import subprocess
import numpy as np
from keras import backend as K

app = Flask(__name__)
api = Api(app)

types = {1: np.int8, 2: np.int16, 4: np.int32}

# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))

""" Windowing and feature extraction """

def open_wav(path_to_wav):
    wav = wave.open(path_to_wav, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    content = wav.readframes(nframes)

    samples = np.fromstring(content, dtype=types[sampwidth])
    return (nchannels, sampwidth, framerate, nframes, comptype, compname), samples

def pad_sequence(x, ts):
    xp = []
    for i in range(x.shape[0]):
        x0 = np.zeros((ts, x[i].shape[1]), dtype=float)
        if ts > x[i].shape[0]:
            x0[ts - x[i].shape[0]:, :] = x[i]
        else:
            maxe = np.sum(x[i][0:ts, 1])
            for j in range(x[i].shape[0] - ts):
                if np.sum(x[i][j:j + ts, 1]) > maxe:
                    x0 = x[i][j:j + ts, :]
                    maxe = np.sum(x[i][j:j + ts, 1])
        xp.append(x0)
    return np.array(xp)

def emotion_predict(path):
    wav = open_wav(path)
    (nchannels, sampwidth, framerate, nframes, comptype, compname), samples = wav
    duration = nframes / framerate

    print('channel count', nchannels)
    left = samples[0::nchannels]
    print('left', left)
    print('left shape', left.shape)
    # right = samples[1::nchannels]
    # left_audio = left[int(start * framerate):int(end * framerate)]
    st_features = cf.calculate_features(left, framerate, None).T

    x = []
    for f in st_features:
        if f[1] > 1.e-4:
            x.append(f)
    x = np.array(x, dtype=float)
    tx = []
    tx.append(np.array(x, dtype=float))
    tx = np.array(tx, dtype=float)
    tx = pad_sequence(tx, 32)

    model = load_model('iemocap_acc0.561715.h5',compile=False)
    available_emotions = ['生气', '激动', '紧张', '悲伤']
    predictResult = model.predict(tx)
    #emotion = available_emotions[np.argmax(predictResult)]
    #prob = predictResult[0][np.argmax(predictResult)]

    return predictResult[0].tolist()

parser = reqparse.RequestParser()
parser.add_argument('task')


class audio_emotion_classify(Resource):
    def get(self):
        #abort_if_todo_doesnt_exist(todo_id)
        #audio_file_path = request.form['data']
        return "get ok"

    def put(self):
        audio_file_path = request.form['data']
        result = emotion_predict(audio_file_path)
        K.clear_session()
        return result
##
## Actually setup the Api resource routing here
##
# api.add_resource(TodoList, '/todos')
api.add_resource(audio_emotion_classify, '/audio_emotion_classify')


if __name__ == '__main__':
    app.run(debug=True)
    # print(emotion_predict('audio.wav'))