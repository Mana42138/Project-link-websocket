# Project-link-websocket

Hello, I have made Simple Universal Chatting system for roblox and other games.
I made this cause i saw roblox didn't have a websocket feature Enjoy!

```lua
-- https://your.ip/website.linkhere.com

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

server.sendMessage("Test Hello") -- Sends a message to the server!
server.sendScript('Mana Hub <string:search>', '2 <string:amount of scripts>')
```

Send Messages from Python

```py
import requests

# &server=false = not server message
# &server=true = servr message
message = 'noobs?'
response = requests.get('https://chatting.madsbrriinckbas.repl.co/api/send/?msg='+message+'&server=false')
```
