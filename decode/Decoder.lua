local decode = function(msg, callback)
	local messages = game:GetService("HttpService"):JSONDecode(msg)
	for i, message in ipairs(messages) do
		pcall(callback, message)
	end
end

return {
	decode = decode
}
