config={}

def readConfigFile():
	with open('system.config','r') as f:
	    for line in f:
	        if line[0] != '#':
	          (key,sep,val) = line.partition('=')
	          # if the line does not contain '=', it is invalid and hence ignored
	          if len(sep) != 0:
	              val = val.strip()
	              if str.isdecimal(val):
	              	config[key.strip()] = int(val);
	              else: 
	              	config[key.strip()] = val;
	# print(config)


def main():
	readConfigFile();

def returnValueListAfterStrippingSpaces(val):
	values = []
	returnValues = []
	if(";" in str(val)):
		values = val.split(";")
	else:
		return val;
	for value in values:
		returnValues.append(value.strip())
	return returnValues

def readProperty(key):
	if key == "client_hosts" or key == "replica_hosts":
		host = []
		hostsIps = []
		hostsIps = returnValueListAfterStrippingSpaces(config["hosts"])
		clientHostNumbers = returnValueListAfterStrippingSpaces(config[key])
		# print("host : ",hostsIps);
		for client in clientHostNumbers:
			host.append(hostsIps[int(client)])
		return host
	return returnValueListAfterStrippingSpaces(config[key]);


if __name__ == '__main__':
	main()









