import time
from pathlib import Path

from bottle import run, route, static_file, jinja2_view

import sample_backend

STATIC_PATH = str(Path(__file__).parent / 'static')


@route('/')
def home():
    return static_file('bottle_server.html', Path(__file__).parent)


@route('/simple-reload/')
@jinja2_view('simple-reload.html')
def simple_reloading_page():
    content = sample_backend.foo()
    return {'content': content}


@route('/simple-reload-js/')
@jinja2_view('simple-reload-js.html')
def simple_reloading_page_js():
    content = sample_backend.foo()
    return {'content': content}


@route('/simple-reload-ajax/')
@jinja2_view('ajax-reload.html')
def reloading_page_ajax():
    return {}


@route('/api/content/')
def just_html_content():
    time.sleep(1)
    return sample_backend.foo()


@route('/static/<path:path>')
def server_static(path):
    return static_file(path, root=STATIC_PATH)


@route('/show/')
def show_images():
    return '<img src="static/my_image.png">'


if __name__ == "__main__":
    run(debug=True, reloader=True, port=8989)
