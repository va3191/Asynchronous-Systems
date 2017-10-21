import nacl.hash
import ast
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
	return digest

def checkForResultConsistency(resultproof,res, allReplicaVerifyKeysMap):
		delta= calculateHash(res)
		flag = True	
		validation, hashMaps = validateResultProof(resultproof,allReplicaVerifyKeysMap)
		# print("between this"+str(resultTuple[0])+"this the lenth od the returned tuple")
		if(not validation):
			return False
		for i in range(0, len(hashMaps)):
			if(hashMaps[i] == delta):
				continue
			else:
				flag = False
		return flag

def validateResultProof(resultproof, allReplicaVerifyKeysMap):
	logger.debug("ValidateResultProof function called  with resultProof : "+str(resultproof))
	hashValues=[]
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
			actualResult = ast.literal_eval(result.decode("utf-8"))
		except nacl.exceptions.BadSignatureError:
			# logger.error("key mismatch failed for ", resultproof[length-i-1])
			return (False,None)
		res, op, hs = actualResult
		# hashe= result.decode("utf-8")
	# logger.info("validateResultProof. SUCCESSFULL!! ")
		hashValues.append(hs)
	return (True,hashValues)


if __name__ == '__main__':
	main()
	








