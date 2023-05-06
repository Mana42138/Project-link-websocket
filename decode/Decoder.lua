local module = {}
module.decode = function(msg, callback)
	local messages = game:GetService("HttpService"):JSONDecode(msg)
	for i, message in pairs(messages) do
		pcall(callback, message)
	end
end
module.decodeScript = function(data, callback)
	local messages = game:GetService("HttpService"):JSONDecode(data)
	for i, message in pairs(messages) do
		pcall(callback, message)
	end
end
return module
