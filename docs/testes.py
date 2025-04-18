"""import json
data = {}
with open("credentials(exemplo).json", 'r') as file:
    data = json.load(file)

file.close()

print(data, type(data))

print(list(data))
    

a = 1"""
"""
a = 'http://localhost:500/?error=cyjhgvzkbypn7y89iwl1otnnxtxmzt&scope=clips%3Aedit+user%3Awrite%3Achat'

b = a.find("?code=")
print(b)
print(a[b:])


# Faz todo o negocio do servidor
# Response: http://localhost:3000/?code=gulfwdmys5lsm6qyz4xiz9q32l10&scope=channel%3Amanage%3Apolls+channel%3Aread%3Apolls&state=c3ab8aa609ea11e793ae92361f002671

# http://localhost:3000/?error=access_denied&error_description=The+user+denied+you+access&state=c3ab8aa609ea11e793ae92361f002671
pass"""

uri = "http://localhost:500"
i_ = len(uri) - uri[::-1].find(":")
port = int(uri[i_:])

i = uri.find("//") + 2 
_i = len(uri[i:]) - len(str(port)) - 1 
host = uri[i:][:_i]

print(port) 
print(host)