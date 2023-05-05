import requests

# &server=false = not server message
# &server=true = servr message
message = 'noobs?'
response = requests.get('https://chatting.madsbrriinckbas.repl.co/api/send/?msg='+message+'&server=false')
