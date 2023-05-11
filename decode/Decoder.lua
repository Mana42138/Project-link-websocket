local module = {}
local http = game:GetService("HttpService")
local message_table = {}

module.decode = function(msg, callback)
	for i,v in pairs(msg) do
		for i,v in pairs(v) do
				table.insert(message_table, v)
				pcall(callback, message_table)
				return message_table
		end
	end
	table.clear(message_table)
end

module.decodeScript = function(data, callback)
	for i,v in pairs(data) do
		for i,v in pairs(v) do
			pcall(callback, v)
		end
	end
end

module.decodeChat = function(data, callback)
	for i, message in pairs(data) do
		pcall(callback, message)
	end
end

function module.isScript(data)
	for i,v in pairs(data) do
		for i,v in pairs(v) do
			return v.isScript
		end
	end
end

function module.getscriptdata(data, callback)
	for i,v in pairs(data) do
		pcall(callback, v)
	end
end

return module
