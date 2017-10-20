import nacl.hash
import logging as logger
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
	logger.basicConfig(
		format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
		handlers=[
		logger.FileHandler("{0}/{1}.log".format(readProperty("logfile_path"), readProperty("logfile_name"))),
		logger.StreamHandler()
		],
		level=logger.DEBUG)


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

def calculateHash(message):
	HASHER = nacl.hash.sha256
	# could be nacl.hash.sha512 or nacl.hash.blake2b instead
	message ="varun os trying to do something"
	msg =str.encode(message)
	# define a 1024 bytes log message
	msg = 16*msg
	digest = HASHER(msg, encoder=nacl.encoding.HexEncoder)

	# now send msg and digest to the user
	print(nacl.encoding.HexEncoder.encode(msg))
	print(digest)
	return digest

def validateResultProof(resultproof, allReplicaVerifyKeysMap):
	logger.debug("ValidateResultProof : "+str(resultproof))
	for i in range(0,len(resultproof)):
		try:
			length = len(resultproof)

			# Create a VerifyKey object from a hex serialized public key
			verify_key = nacl.signing.VerifyKey(allReplicaVerifyKeysMap[length-i-1], encoder=nacl.encoding.HexEncoder)
			# logger.debug("result number",i+1, "from result proof", resultproof[length-i-1])
			message = resultproof[length-i-1]
			# Check the validity of a message's signature
			# Will raise nacl.exceptions.BadSignatureError if the signature check fails
			result = verify_key.verify(message)

			# logger.debug("verified")
			actualResult = result.decode("utf-8")
		except nacl.exceptions.BadSignatureError:
			# logger.error("key mismatch failed for ", resultproof[length-i-1])
			return (False,None)
	# logger.info("validateResultProof. SUCCESSFULL!! ")
	return (True,actualResult)


if __name__ == '__main__':
	main()
	








