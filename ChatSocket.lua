local decode = require(script.decode)

local ws = function(dict)
	local channel = dict.channels or {"general"}
	local API = dict.url or 'https://chatting.madsbrriinckbas.repl.co/api/'
	local server = game:GetService("HttpService")
	local onMessage = dict.onMessage or function(msg)
		print(msg)
		if dict:isScript(msg) then
			decode.decode(msg, function(t) -- Default decode
				print(t)
			end)
		else
			decode.decodeScript(msg, function(t) -- Default decode
				print(t)
			end)
		end
	end
	local function sendMessage(data)
		local data = data or {}
		local encode_data = {
			msg = data.msg,
			server = data.server,
			Discord = data.DCName,
			ID = data.ID
		}
		server:PostAsync(API..'send/', server:JSONEncode(encode_data), Enum.HttpContentType.ApplicationJson)
	end
	
	local function sendScript(data)
		local encode_data = {
			search = data.search,
			plr = data.plr,
			ID = data.ID,
			value = data.value
		}
		server:PostAsync(API..'script_search', server:JSONEncode(encode_data), Enum.HttpContentType.ApplicationJson)
	end
	
	local loop = coroutine.create(function()
		while wait(1) do
			for i,v in pairs(channel) do
				local msg
				msg = server:JSONDecode(server:PostAsync(API..'poll/', server:JSONEncode({ID = v}), Enum.HttpContentType.ApplicationJson))
				if msg ~= nil and msg ~= {} then
					onMessage(msg)
				end
			end
		end
	end)
	coroutine.resume(loop)
	
	return {
		Url = API,
		channels = channel,
		onMessage = onMessage,
		sendMessage = sendMessage,
		sendScript = sendScript
	}
end

return ws
