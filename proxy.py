import requests
import json
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def catch_all_get(path):
    url = create_url(path, request.args.get('host'))

    try:
        response = requests.get(url)
    except Exception as error:
        print("ERROR", error)
    finally:
        print(url)

    if 'json' in response.headers["content-type"]:
        return json.dumps(json.loads(response.content.decode('utf-8')), ensure_ascii=False)
    else:
        return response.content


@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def catch_all_post(path):
    url = create_url(path, request.args.get('host'))

    try:
        response = requests.post(url, data=request.json)
    except Exception as error:
        print("ERROR ", error)
    finally:
        print(url)
        print(" with body {body}".format(body=request.json))

    return response.json()


def create_url(path, host):
    url = 'https://{host}/{path}?{query_string}'.format(
        host=host,
        path=path,
        query_string=request.query_string.decode('ascii')
    )
    return url


if __name__ == '__main__':
    app.run()
