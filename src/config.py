import nacl.encoding
import nacl.hash
import ast
import logging as logger
import ast
import sys
import getopt
import hashlib
import random

config={}
def readConfigFile(configFile):
	with open(configFile,'r') as f:
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

config={}

def config_main(filePath):
	print("HERE config_mainconfig_mainconfig_mainconfig_mainconfig_mainconfig_main")
	readConfigFile(filePath);
	logger.basicConfig(
		format="%(asctime)s [%(threadName)-12.12s %(lineno)d] [%(levelname)-5.5s]  %(message)s",
		handlers=[
		logger.FileHandler("{0}/{1}.log".format(readProperty("logfile_path"), readProperty("logfile_name"))),
		logger.StreamHandler()
		],
		level=logger.INFO)
	# readFailures()


def returnValueListAfterStrippingSpaces(key,val):
	values = []
	returnValues = []
	if("workload" in key and ";" not in str(val)):
		returnValues.append(val)
		return returnValues
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
		hostsIps = returnValueListAfterStrippingSpaces(key,config["hosts"])
		clientHostNumbers = returnValueListAfterStrippingSpaces(key,config[key])
		# print("host : ",hostsIps);
		for client in clientHostNumbers:
			host.append(hostsIps[int(client)])
		return host

	if "workload" in key and "pseudorandom" in config[key]:
		value = config[key]
		tpl = value.split("pseudorandom")[1]
		tupl = ast.literal_eval(tpl)
		seed=tupl[0]
		n=tupl[1]
		mod=5
		return pseudorandom(seed,n,mod)
	
	return returnValueListAfterStrippingSpaces(key,config[key]);

def readFailures():
	failureText='failures'
	val = []
	configurationNumber=int()
	replicaNumber=int()
	# triggerList=["client_request","forwarded_request","shuttle","result_shuttle"]
	failureDS = {}
	# failureDS["triggers"]=triggerList
	'''
	{
		"triggers":["client_request","forwarded_request","shuttle","result_shuttle"],

		"$configurationNumber" : {
			"replica" : [
				"$replicaNumber" : {
					"client" : "$clientNumber"
					"messageNumber" : "$messageNumber"
					"triggerName" : "$triggerName"
					"triggerFailure" : "$triggerFailure"
				}
			]
			"client" : [
				"$clientNumber" : {
					"replica" : "$clientNumber"
					"messageNumber" : "$messageNumber"
					"triggerName" : "$triggerName"
					"triggerFailure" : "$triggerFailure"
				}
			]
		}
	}

	'''

	for key,value in config.items():
		if("failures" in key):
			failureListKey = key.split("failures")[1]
			failureListKeyList = ast.literal_eval(failureListKey)
			configurationNumber=failureListKeyList[0]
			replicaNumber=failureListKeyList[1]
			replicaArray=[]
			
			if(configurationNumber not in failureDS):
				failureDS[configurationNumber]={}

			if("replica" not in failureDS[configurationNumber]):
				failureDS[configurationNumber]["replica"]={}

			if(replicaNumber not in failureDS[configurationNumber]["replica"]):
				failureDS[configurationNumber]["replica"][replicaNumber]=[]

			# print("replicaNumber : ",replicaNumber, ", failureDS : ",failureDS," failureDS[configurationNumber][replica]: ",failureDS[configurationNumber]["replica"][replicaNumber])
			failureValueList = value.split(";")
			
			for failureValue in failureValueList:
				replicaOperation={}
				trigger,failure = failureValue.split("),")
				trigger +=')'
				triggerName = trigger.split('(')[0]
				triggerValuetemp = trigger.split(triggerName)[1]
				triggerValuetempList = ast.literal_eval(triggerValuetemp)
				clientNumber,messageNumber = triggerValuetempList			
				replicaOperation["client"]=clientNumber
				replicaOperation["messageNumber"]=messageNumber
				replicaOperation["triggerName"]=triggerName
				if("()" in failure):
					replicaOperation["triggerFailure"]=failure.split("()")[0]
				else:
					replicaOperation["triggerFailure"]=failure.split("(")[0]
					replicaOperation["triggerFailure_m"]=failure.split("(")[1].split(")")[0]
				# print('failure.split("()")[0]: ',failure.split("()")[0],"===> ", failure)
				failureDS[configurationNumber]["replica"][replicaNumber].append(replicaOperation)

	logger.info("failures defined in config file failureDS :"+str(failureDS));#+", replicaNumber: "+str(replicaNumber)+", triggerName : "+triggerName+", clientNumber : "+str(clientNumber)+"=> messageNumber : "+str(messageNumber)+", failure : "+failure)
	

	# 	log.info("possible failures in config file failureDS :"+", replicaNumber: "+str(replicaNumber)+", triggerName : "+triggerName+", clientNumber : "+str(clientNumber)+"=> messageNumber : "+str(messageNumber)+", failure : "+failure)
	#,", failureValueList : ",failureValueList)
	return failureDS

def calculateHash(message):
	HASHER = nacl.hash.sha256
	# could be nacl.hash.sha512 or nacl.hash.blake2b instead
	msg =str.encode(message)
	# define a 1024 bytes log message
	msg = 16*msg
	digest = HASHER(msg, encoder=nacl.encoding.HexEncoder)

	# now send msg and digest to the user
	return digest

def checkForResultConsistency(resultproof,res, allReplicaVerifyKeysMap, source):
		delta= calculateHash(res)
		quorum=0
		print("inside here")
		validCount=0
		if(source == "replica"):
			quorum= (2*int(config['t'])) +1
		elif(source=="client"):
			quorum = int(config['t']) +1

		# print("the delta value of res:" + str(res) + " :delta:"+str(delta))
		flag = False	
		if(source =="client"):
			validation, hashMaps = validateResultProofClient(resultproof,allReplicaVerifyKeysMap)
		elif(source =="replica"):
			validation, hashMaps = validateResultProof(resultproof,allReplicaVerifyKeysMap)
		print("validation : ", validation)
		# print("between this"+str(resultTuple[0])+"this the lenth od the returned tuple")
		if(not validation):
			return False
		for i in range(0, len(hashMaps)):
			if(hashMaps[i] == delta):
				validCount= validCount+1
				continue
		
		if(validCount>=quorum):
			flag=True
		print ("the flag returned is  ", flag)
		return flag

def validateResultProof(resultproof, allReplicaVerifyKeysMap):
	logger.debug("ValidateResultProof function called  with resultProof : "+str(resultproof))
	hashValues=[]
	if(resultproof==None):
		return False,None
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

def randomNum(l):
	a = random.randint(0,l)
	b= random.randint(0,l)
	if a<b:
		return a,b
	else:
		return b,a

def operationSpace(numArr):
	operList=["get","put","slice","append"]
	operations=[]
	for i in range(numArr): 
		oper=operList[i%4]
		temp={}
		tempstr=oper + "('key" +str(i)+"'"
		if(oper =='get'):
			tempstr=tempstr+")"
		elif(oper =='put'):
			temp["key"+str(i)]="value"+str(i)
			tempstr = tempstr+",'"+str(temp["key"+str(i)])+"')"
		elif(oper == "slice"):
			a,b =randomNum(6)
			tempstr= tempstr +",'" +str(a)+":"+str(b)+"')"
		elif(oper =='append'):
			temp["key"+str(i)]="value"+str(i)
			tempstr = tempstr+",'"+str(temp["key"+str(i)])+"')"


		operations.append(tempstr)
	return operations

def repeatable_random(seed , n,mod):

	seed = random.seed(seed)
	randomNumbers = []
	while(n>0):
		seed = random.randint(0, mod-1)
		randomNumbers.append(seed)
		n=n-1
	return randomNumbers
	# print("randomNumbers : "+str(randomNumbers))

def pseudorandom(seed,n,mod):
	operations=operationSpace(mod)
	randomNumbers = repeatable_random(seed,n,mod)
	finalOperations=[]
	for i in range(0,n):
		# print("randomNumber : "+randomNumbers[i])
		finalOperations.append(operations[randomNumbers[i]])

	# print("======>","".join(finalOperations))
	return finalOperations

# def executeOperationForClient(request_id,operation,dictionary_data):
	

def executeOperation(request_id,operation,dictionary_data):
	logger.info("Executing Operation in dictonary. operation : "+str(operation))
	temp=operation.split('(')
	result = ''
	if(temp[0]=="put"):
		tempsplit=operation.split('\'')
		dictionary_data[tempsplit[1]]=tempsplit[3]
		result='ok'

	elif(temp[0] == "append"):
		tempsplit=operation.split('\'')
		if(tempsplit[1] in dictionary_data):
			dictionary_data[tempsplit[1]] = dictionary_data[tempsplit[1]] + ' ' + tempsplit[3]
			logger.debug('append is executeed@@@@@@@@')
			result= 'ok'
		else:
			result= 'fail'

	elif(temp[0] == "get"):
		tempsplit=operation.split('\'')
		if(tempsplit[1] in dictionary_data):
			value = dictionary_data[tempsplit[1]];
			result= value
			logger.debug('get is executeed@@@@@@@@')	
		else:
			result= ''

	elif(temp[0] == "slice"):
		tempsplit=operation.split('\'')
		# logger.info("After Executing Operation in dictonary. => "+str(tempsplit))
		# logger.info("str(tempsplit[1]) => "+str(tempsplit[1]))
		# logger.info("str(dictionary_data[tempsplit[1]]) => "+str(dictionary_data[tempsplit[1]]))
		if(tempsplit[1] in dictionary_data):
			ind  = tempsplit[3].split(':')
			if (len(dictionary_data[tempsplit[1]])) > int(ind[1]):
				dictionary_data[tempsplit[1]] = dictionary_data[tempsplit[1]][int(ind[0]):int(ind[1])]
				result= 'ok'
			else:
				result= 'fail'
		else:
			result= 'fail'
		# logger.info("slice operation successfully executed")
	return result



def validateResultProofClient(resultproof, allReplicaVerifyKeysMap):
	logger.debug("ValidateResultProof function called  with resultProof : "+str(resultproof))
	hashValues=[]
	if(resultproof==None):
		return False,None
	# case=''
	# i=0
	# length = len(resultproof)
	# if(len(resultproof)==config['num_replica']):
	# 	index = length-i-1
	# elif(len(resultproof)<config['num_replica']):
	# 	index=length - i
	for i in range(0,len(resultproof)):
		try:
			length = len(resultproof)

			# Create a VerifyKey object from a hex serialized public key
			if(len(resultproof)==   (2*int(config['t'])) +1):
				verify_key = nacl.signing.VerifyKey(allReplicaVerifyKeysMap[length-i-1], encoder=nacl.encoding.HexEncoder)
			elif(len(resultproof)<(2*int(config['t'])) +1):
				verify_key = nacl.signing.VerifyKey(allReplicaVerifyKeysMap[length-i], encoder=nacl.encoding.HexEncoder)
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

def getUnsignedData(operation_en,client,clientVerifyKeys,clients):
		logger.debug("getUnsignedData for operation_en : "+str(operation_en))
		# request_id=''
		operation=''
		try:
			index =clients.index(client)
			verify_key = nacl.signing.VerifyKey(clientVerifyKeys[index], encoder=nacl.encoding.HexEncoder)
			# tempId = verify_key.verify(request_id_en)
			tempId1 = verify_key.verify(operation_en)
			# request_id = tempId.decode("utf-8")
			operation = tempId1.decode("utf-8")
		except  nacl.exceptions.BadSignatureError:
			logger.error("operation_en: "+operation_en+", client signed operation not valid detected at olympus")
		logger.debug("unsigned successfully at olympus")
		return operation



