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

@app.route("/api/send/", methods=["POST"])
def send():
    data = request.get_json()
    isserver = data["server"]
    message = data["msg"]
    discord_name = data["Discord"]
    channelid = data["ID"]
    uniqe_id = ''.join(random.choice(string.hexdigits) for i in range(12)) # so that it doesn't get deleted if someone types the same thing :)

    mess = readfile(data_file)
    messages = mess['Messages']

    table = messages.get(str(channelid))
    if not table:
        table = {}
        messages[str(channelid)] = table

    if isserver == 'false':
        table[uniqe_id] = {'msg': message, 'Discord': discord_name, 'isScript': False, 'success': True}
    else:
        table[uniqe_id] = {'msg': 'Server: '+message, 'Discord': '_Server_', 'isScript': False, 'success': True}

    writefile(data_file, mess)
    
    return {'success': True, 'status': 200}

@app.route('/api/script_search/', methods=['POST'])
def script():
    request_data = request.get_json()
    searched = request_data["search"]
    plr = request_data["plr"]
    channelid = request_data["ID"]
    value = int(request_data["value"])
    uniqe_id = ''.join(random.choice(string.hexdigits) for i in range(12))
    
    mess = readfile(data_file)
    messages = mess['Messages']

    table = messages.get(str(channelid))
    if not table:
        table = {}
        messages[str(channelid)] = table
        writefile(data_file, mess)


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
            "Verified": script["verified"],
            'success': True,
            'Player': plr
        }
        fields[script["game"]["name"]] = field

    table[uniqe_id] = {'data': fields, 'isScript': True,}
    
    writefile(data_file, mess)

    return {'success': True, 'status': 200}

# @app.route('/api/channel/', methods=['POST'])
# def channel():
#     request_data = request.get_json()
#     channelid = request_data["ID"]

#     read_data_file = readfile(data_file)
#     messages = read_data_file['Messages']
#     table = messages.get(str(channelid))
#     if not table:
#         messages[channelid] = {}
#         return {'success': False}
#     return {'success': True, 'data': table}

@app.route('/api/poll/', methods=["POST"])
def poll():
    request_data = request.get_json()
    channelid = request_data.get("ID")
    mess_list = []
    mess = readfile(data_file)
    messages2 = mess['Messages']
    table = messages2.get(str(channelid))
    if table:
        messages = mess["Messages"][channelid]
    else:
        mess["Messages"][channelid] = {}
        messages = mess["Messages"][channelid]
        writefile(data_file, mess)
    
    for i, msg in messages.items():
        if 'msg' in msg:
            mess_list.append(msg)
        elif 'data' in msg:
            mess_list.append(msg)

    messages2.clear()
    writefile(data_file, mess)
    response_data = {'messages': mess_list}
    return json.dumps(response_data)


async def start_server():
    app.run(port=9090, host='0.0.0.0')

    # keep alive loop!
    while True:
        print('loop')
        await asyncio.sleep(10)


asyncio.run(start_server())
