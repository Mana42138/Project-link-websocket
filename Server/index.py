from flask import Flask, request
import asyncio
import random, string
import json, os

data_file = 'chatting/data.json'

def readfile(data_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
    return data
def writefile(data_file, data):
    with open(data_file, 'w') as f:
        data = json.dump(data, f, indent=4)
    return data

if not os.path.exists(data_file):
    new_data = {
        'Messages': {}
    }
    writefile(data_file, new_data)

app = Flask(__name__)

@app.route("/api/send/", methods=["GET"])
def send():
    data = str(request.args.get('msg'))
    isserver = request.args.get('server')
    uniqe_id = ''.join(random.choice(string.hexdigits) for i in range(12)) # so that it doesn't get deleted if someone types the same thing :)

    mess = readfile(data_file)
    print(mess)
    messages = mess['Messages']

    if isserver == 'false':
        messages[uniqe_id] = {'msg': data}
    else:
        messages[uniqe_id] = {'msg': 'Server: '+data}

    writefile(data_file, mess)
    
    return {'success': True, 'status': 200}

def deletemsg(id):
    mess = readfile(data_file)
    messages = mess['Messages']

    print(messages[id])

    del messages[id]

@app.route('/api/poll/', methods=["GET"])
def poll():
    mess_list = []
    mess = readfile(data_file)
    messages = mess['Messages']
    
    for i, msg in messages.items():
        if 'msg' in msg:
            mess_list.append(msg['msg'])
        else:
            return None
    
    # delete all messages from the dictionary
    messages.clear()
    writefile(data_file, mess)
    if mess_list == '[]':
        return None
    return mess_list

async def start_server():
    app.run(port=9090, host='0.0.0.0')

    # keep alive loop!
    while True:
        print('loop')
        await asyncio.sleep(10)


asyncio.run(start_server())
