# Project-link-websocket

Hello, I have made Simple Universal Chatting system for roblox and other games.
I made this cause i saw roblox didn't have a websocket feature Enjoy!

```lua

local Socket = require(game.ReplicatedStorage.ChatSocket)
local decode = require(game.ReplicatedStorage.ChatSocket.decode)

function isScript(data) data = http:JSONDecode(data) for i,v in pairs(data) do return v.isScript end end

local server = Socket({
	url = "https://your.ip/website.linkhere.com/api/",
	onMessage = function(msg)
		if not isScript(msg) then
			decode.decode(msg, function(msg)
				DataEvent:FireAllClients(msg.msg, "FireClient")
			end)
		else
			decode.decodeScript(msg, function(data)
				SearchEvent:FireAllClients(data)
			end)
		end
	end
})

local Socket = require(game.ReplicatedStorage.ChatSocket)
local decode = require(game.ReplicatedStorage.ChatSocket.decode)

local server = Socket({
	url = "https://your.ip/website.linkhere.com/api/",
	channels = {
		"general"
	},
	onMessage = function(msg)
		if not decode.isScript(msg) and msg.messages ~= {} then
			decode.decode(msg, function(msg)
				DataEvent:FireAllClients(msg, "FireClient")
			end)
		end
		if decode.isScript(msg) then
			decode.decodeScript(msg, function(data)
				SearchEvent:FireAllClients(data.data)
			end)
		end
	end
})



server.sendMessage({
	msg = 'Hello World!',
	server = 'false',
	DCName = 'a username', -- i use peoples discord name not releasing that api tho
	ID = 'general'
}) -- Sends a message to the server!

server.sendScript({
	search = 'Mana Hub <string:search>', -- Search for a Script name Not game name.
	plr = plr.Name, -- Player Name
	ID = 'general', -- Channel ID
	value = '2 <string:amount of scripts>' -- How many scripts you want to search for.
})
```

Send Messages from Python

```python
import requests
API = "https://your.ip/website.linkhere.com/api/"
payload = {
    'search' : "Project Link",
    'value' : "2",
    'plr' : 'Test#9724',
    'ID' : 'general'
}

response = requests.post(f'{API}script_search/', json=payload)

data = {
    'msg': "fuck you",
    'server': 'false',
    'Discord': 'Test',
    'ID' : 'general'
}
response = requests.post(f'{API}send/', json=data).json()

data = {
    'ID' : 'general'
}
response = requests.post(f'{API}poll/', json=data).json()
print(response)
```
