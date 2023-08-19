from flask import Flask, template_rendered, render_template, send_file, make_response, request
from werkzeug.datastructures import Headers
import os
import re
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

app = Flask(__name__)

root_dir = "I:\\录制"
pic_pattern = re.compile(r'\.(jpg|jpeg|png|gif|bmp)$', re.IGNORECASE)
video_pattern = re.compile(r'\.(mp4|avi|rmvb|rm|flv|wmv|mkv)$', re.IGNORECASE)

def render(path):
    abs_path = os.path.join(root_dir, path)

    if not os.path.exists(abs_path):
        return "path not exists"

    if os.path.isdir(abs_path):

        files = os.listdir(abs_path)


        folders = []
        videos = []
        pics = []

        for file in files:
            if os.path.isdir(os.path.join(abs_path, file)):
                folders.append(file)
            elif pic_pattern.search(file):
                pics.append(file)
            elif video_pattern.search(file):
                videos.append(file)

        return render_template('index.html', folders=folders, videos=videos, pics=pics, path=path, ip=ip_address)
    else:
        if(video_pattern.search(abs_path)):
            range_header = request.headers.get('Range', None)
            if range_header:
                match = re.search(r'bytes=(\d+)-\d*', range_header)
                sk = int(match.group(1))
            else:
                sk = 0

            cwd = os.getcwd()

            with open(abs_path, 'rb') as fr:
                fr.seek(0, 2)
                total = fr.tell()
                fr.seek(sk)
                chunk = fr.read(1024 * 1024 * 2)
                end = sk + len(chunk) - 1
                headers = Headers()
                headers.add('Accept-Ranges', 'bytes')
                headers.add('Content-Type', 'application/octet-stream')
                headers.add('Content-Range', 'bytes {}-{}/{}'.format(sk, end, total))
                return make_response(chunk, 206, headers)
        else:
            return send_file(abs_path)




@app.route('/')
def index():  # put application's code here
    return render('')

@app.route('/<path:path>')
def detail_path(path):

    return render(path+'/')

if __name__ == '__main__':


    app.run(host="0.0.0.0",port= 80)
