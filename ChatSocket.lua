local decode = require(script.decode)

local ws = function(dict)
	local API = dict.url or 'https://chatting.madsbrriinckbas.repl.co/api/'
	local server = game:GetService("HttpService")
	local onMessage = dict.onMessage or function(msg)
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
	local function sendMessage(msg)
		server:GetAsync(API..'send/?msg='..tostring(msg)..'&server=false')
	end
	
	local function sendScript(search, value, plr)
		local plr = plr or ''
		server:GetAsync(API..'script_search?search='..search..'&val='..value..'&plr='..plr)
	end
	
	local loop = coroutine.create(function()
		while wait(1) do
			local msg = server:GetAsync(API..'poll/')
			if msg ~= 'None' then
				for i,v in pairs(server:JSONDecode(msg)) do
					if v.isScript == false then
						onMessage(msg)
					else
						onMessage(msg)
					end
				end
			end
		end
	end)
	coroutine.resume(loop)
	
	return {
		Url = API,
		onMessage = onMessage,
		sendMessage = sendMessage,
		sendScript = sendScript
	}
end

return ws
