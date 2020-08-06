import os
import json
import ffmpeg
import requests
from bot import token
from flask import Flask
from pathlib import Path
from detect_faces import Detector

app = Flask(__name__)

d = Detector()


@app.route('/api/voice/<file_path>/<uid>', methods=['GET'])
def api_voice(file_path, uid):
    try:
        file = requests.get('https://api.telegram.org/file/bot{0}/voice/{1}'.format(token, file_path))
    except:
        return 'error'
    else:
        Path('static/voices/' + uid).mkdir(parents=True, exist_ok=True)
        path = os.path.join('static', 'voices', uid, file_path)

        with open(path, 'wb') as f:
            f.write(file.content)

        out_path = os.path.join('static', 'voices', uid, 'audio_message_' + str(counter(uid)))
        decode_audio(path, out_path)
        os.remove(path)
        out_path = out_path + '.wav'
        return out_path.replace('\\', '/')


@app.route('/api/photos/<file_path>/<uid>', methods=['GET'])
def api_photo(file_path, uid):
    try:
        file = requests.get('https://api.telegram.org/file/bot{0}/photos/{1}'.format(token, file_path))
    except:
        return 'error'
    else:
        Path('static/photos/' + uid).mkdir(parents=True, exist_ok=True)
        path = os.path.join('static', 'photos', uid, file_path)

        if d.detect_face(file.content):
            with open(path, 'wb') as f:
                f.write(file.content)
            return path.replace('\\', '/')
        else:
            return 'error'


def decode_audio(in_filename, o_filename):
    input = ffmpeg.input(in_filename)
    out = ffmpeg.output(input, o_filename + '.wav', format='wav', acodec='pcm_s16le', ac=1, ar='16000') \
        .overwrite_output()\
        .run()
    return out


def counter(uid):
    with open('counters.json', 'r+') as f:
        pairs = json.loads(f.read())
        if uid in pairs:
            pairs[uid] = pairs[uid] + 1
        else:
            pairs.setdefault(uid, 0)
        print(type(pairs))
        f.seek(0)
        f.truncate()
        json.dump(pairs, f, ensure_ascii=False)
        return pairs[uid]


if __name__ == '__main__':
    app.run()
