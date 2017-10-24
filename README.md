Asynchronous-Systems CSE 535
Byzantine Chain Replication HMAC


System Requirements:	
DistAlgo - 
pyDistAlgo. Version: 1.0.9


Python
Version 3.4 or above
Python pynacl module


OS
MacOS Yosemite - 10.10.4


Installing of Software:
The following command installs DistAlgo as system-wide package:

<Installing Python>
cd <DAROOT>; python setup.py install 

<Python module for signature of keys>
pip install pynacl

## INSTRUCTIONS
Build: python3.6 -m da.compiler <filename>
Run: python3.6 -m da -n <node name> <da file> <configuration file name>
In above command, replace <node name> with node process, <dafile> with da file containing main method and <configfilename> with config file name


##RUNNING DISTALGO
RunSystem.da is the main file for running the whole distalgo project Byzantine chain replication project. The file RunSystem is run as “main” node. Example of commands

python3 -m da -n main RunSystem.da -i system.config 

-m : argument for providing the option to run Distalgo files.
-n : name of the node
RunSystem.da : name of the file
-i : parameter defines the config file(system.config) to pick while running the project.


Example:
Commands 1 to 6 are used for running a sample program using config file system.config

	1.) python3 -m da -n main RunSystem.da -i system.config 
				-i parameter helps to define the particular config file. It contains properties specific to retransmission, like
				sleep time at replica, retransmission counter, client timeout specific to retransmission, which will trigger retransmission.
	2.) python3 -m da -n client_0  -D RunSystem.da 
	3.) python3 -m da -n client_1 -D RunSystem.da 
	4.) python3 -m da -n replica_0 -D RunSystem.da  
	5.) python3 -m da -n replica_1  -D RunSystem.da 
	6.) python3 -m da -n replica_2 -D RunSystem.da 
Description:
	Config file = system.config
	t byzantine failure=1
	client=2
	replica=3
configuration_file_name
	system.config 
NOTE: -D is specifically added to avoid that particular replica to run its Main

Commands:


##Project Structure

“src” - contains files - RunSystem.da, Client.da, Olympus.da, Replica.da, config.py
“config” - contains configuration files, including test cases.
“logs” - contains log file
“pseudocode” - contains pseudocode from phase-1
ReadMe.md
testing.txt 


PSEUDORANDOM WORKLOAD
We used python random module. Given 2 numbers (seed, n) where n is the total number of operations and seed is the initial seed number accepted by random module. The random number given by the random module is again seed back for generating the next random number. We made a pool of all the 4 operations [ get, append, slice, put]. The pool is configurable by any given number. The random number generated picks the operation from pool and generates a sequence of n operations.


MULTIHOST 
Running the program on two host adityatomer and 'vagarwal'. Starting with the 'onode' on host adityatomer, listening on interfaces:

adityatomer> python3.6 -m da -H 0.0.0.0 -n onode RunSystem.da ../config/system.config

Starting 'replica_0', 'replica_1', 'replica_2' on host vagarwal, connecting the node on adityatomer  one by one

vagarwal> python3.6 -m da -H 0.0.0.0 -R adityatomer -n replica_0 -D RunSystem.da ../config/system.config
vagarwal> python3.6 -m da -H 0.0.0.0 -R adityatomer -n replica_1 -D RunSystem.da ../config/system.config
vagarwal> python3.6 -m da -H 0.0.0.0 -R adityatomer -n replica_2 -D RunSystem.da ../config/system.config

Starting 'client0' on host 'adityatomer', and connecting to the node on 'vagarwal'

adityatomer> python3 -m da -H 0.0.0.0 -R vagarwal -n client_0 -D RunSystem.da ../config/system.config


ASSUMPTIONS:
There wont be any kind of failures in failure scenarios itself. (failure scenarios should work as expected)



BUGS AND LIMITATIONS
In case of retransmission by a client. If all the replicas send the request to the head in this  case if the response is not found in cache. The head never sends the request from the cache.
In order to mock the retransmission, the tail replica sleeps for more time than the client timeout. The client send the retransmission request at all the replicas, the replica forward the request to head and head start the protocol from scratch, the retransmission request again timeout.
In case of multiple client, the verification of dictionary object at client side is not supported, Hence their can be concurrency issues.


## CONTRIBUTION
The project was equally contributed by Aditya Tomer and Varun Agarwal
111491232
111491409


