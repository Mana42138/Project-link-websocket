local decode = require(script.decode)

local ws = function(dict)
	local API = dict.url or 'https://chatting.madsbrriinckbas.repl.co/api/' --you can also paste you link here if you dont want to show it in the Socket table!
	local server = game:GetService("HttpService")
	local onMessage = dict.onMessage or function(msg)
		decode.decode(msg, function(t)
			print(t)
		end)
	end
	local function sendMessage(msg)
		server:GetAsync(API..'send/?msg='..tostring(msg)..'&server=false')
	end
	
	local loop = coroutine.create(function()
		while wait(1) do
			local msg = server:GetAsync(API..'poll/')
			if msg ~= '[]\n' then
				onMessage(msg)
			end
		end
	end)
	coroutine.resume(loop)
	
	return {
		Url = API,
		onMessage = onMessage,
		sendMessage = sendMessage
	}
end

return ws
