# Project-link-websocket

Hello, I have made Simple Universal Chatting system for roblox and other games.
I made this cause i saw roblox didn't have a websocket feature Enjoy!

## I used Python for the Socket

```lua
local Socket = require(game.ReplicatedStorage.ChatSocket) -- Remmember to rename the path to the ChatSocket
local decode = require(game.ReplicatedStorage.ChatSocket.decode) -- Remmember to rename the path to the decoder
local server = Socket({
	url = "https://your.ip/website.linkhere.com" -- i am using repl.it for mine,
	onMessage = function(msg)
		decode.decode(msg, function(msg)
			DataEvent:FireAllClients(msg, "FireClient")
			print(msg)
		end)
	end,
})

server.sendMessage("Test Hello") -- Sends a message to the server!
```
