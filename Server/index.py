from flask import Flask, request
import asyncio
import random, string
import json, os
import requests

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
    messages = mess['Messages']

    if isserver == 'false':
        messages[uniqe_id] = {'msg': data, 'isScript': False}
    else:
        messages[uniqe_id] = {'msg': 'Server: '+data, 'isScript': False}

    writefile(data_file, mess)
    
    return {'success': True, 'status': 200}

@app.route('/api/script_search/', methods=['GET'])
def script():
    searched = str(request.args.get('search'))
    value = int(request.args.get('val'))
    plr = str(request.args.get('plr'))
    uniqe_id = ''.join(random.choice(string.hexdigits) for i in range(12)) # so that it doesn't get deleted if someone types the same thing :)

    data = readfile(data_file)
    messages = data['Messages']

    blox_response = requests.get(f"https://scriptblox.com/api/script/search?q={searched}&mode=free").json()
    scripts = blox_response["result"]["scripts"]

    data_scripts = len(scripts)

    if value > data_scripts:
        value = int(data_scripts)

    random_scripts = random.sample(scripts, value)
    fields = {}
    for script in random_scripts:
        slug = script["slug"]
        field = {
            "name": script["title"],
            "value": script["game"]["name"],
            "script": f"loadstring(game:HttpGet('https://rawscripts.net/raw/{slug}'))()",
            "Verified": script["verified"]
        }
        fields[script["game"]["name"]] = field

    messages[uniqe_id] = {'data': fields, 'isScript': True, 'Player': plr}
    writefile(data_file, data)

    return messages[uniqe_id]

@app.route('/api/poll/', methods=["GET"])
def poll():
    mess_list = []
    mess = readfile(data_file)
    messages = mess['Messages']
    
    for i, msg in messages.items():
        if 'msg' in msg:
            # print(msg)
            mess_list.append(msg)
        elif 'data' in msg:
            mess_list.append(msg)

    print(mess_list)

    messages.clear()
    writefile(data_file, mess)
    if mess_list == []:
        return 'None' # this was the error
    return mess_list

async def start_server():
    app.run(port=9090, host='0.0.0.0')

    # keep alive loop!
    while True:
        print('loop')
        await asyncio.sleep(10)


asyncio.run(start_server())
