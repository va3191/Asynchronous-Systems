## Distributed Key Value Store

### Replication of data in Byzantine environment to enhance fault tolerance

### What is Byzantine Chain Replication? 
Byzantine-tolerant State Machine Replication (BSMR) is the only known generic
approach to making applications tolerate arbitrary faults beyond crash failures
in an asynchronous environment.

### Features

* __Fault_Tolerance :-__ System can bear up to t faulty nodes, still function smoothly
* __Reconfigurable_protocols :-__ protocols that are easily reconfigurable, do not require accurate failure detection, and
are able to tolerate Byzantine failures.
* __Shuttle_Protocol :-__ two simple implementations of Shuttle: one that can
tolerate Byzantine failures in their full generality, and one that tolerates
“accidental failures” such as crashes, bit flips, concurrency bugs

### Why I built this ? 
As part of my course work under Asynchronous Systems (CSE-535)

### System Requirements:	


#### Python

   DistAlgo requires Python version 3.5 or higher, which can be obtained
   from http://www.python.org. This document assumes that your installation
   uses the default name `python` for the Python executable.

   NOTE: If your system has both Python 2.x and Python 3.x installed, your
   Python executable is likely Python 2. In that case, you should replace
   `python` with `python3` (or `pythonX.Y` where 'X.Y' is the exact Python
   version you want to use) in all following command line examples. To find
   out which version of Python is installed on your system, type:

      python --version

#### Operating system

   DistAlgo has been tested on GNU/Linux and Microsoft Windows. The command
   line instructions given in this document use GNU Bash syntax. If you are
   using a different shell (e.g., Windows 'cmd.exe' shell), please adjust the
   commands accordingly.


#### DistAlgo Installation

  Download Distalgo codebase from <https://github.com/DistAlgo/distalgo>. 
  Installation of DistAlgo is entirely optional. The installation process
  consists of copying or extracting the DistAlgo files to a path in the
  local filesystem (designated as `<DAROOT>` in the following texts), then
  adding `<DAROOT>` to `PYTHONPATH` so that Python can load the `da` module.
  You can accomplish this through either one of the following options:

##### Option 1: Using `pip` to install DistAlgo

   `pip` is a command line utility for installing Python packages from the
   Python Package Index(PyPI). `pip` is the recommended method of installing
   DistAlgo. Using `pip`, you do not need to manually download the DistAlgo
   distribution package or setup environment variables, as `pip` will manage
   all of that for you. The name of the DistAlgo package on PyPI is
   'pyDistAlgo'.
   
   To install DistAlgo as a system-wide package:
   
     pip install pyDistAlgo
    
##### Option 2: Using `setup.py`

   If you have already downloaded a DistAlgo distribution package, you can
   install it using the included `setup.py` file. To see full usage
   description, type:

      cd <DAROOT>; python setup.py --help

The following command installs DistAlgo as system-wide package:

      cd <DAROOT>; python setup.py install

##### Option 3: Manually adding the DistAlgo root directory to `PYTHONPATH`

   If you have downloaded and extracted the DistAlgo files to `<DAROOT>`,
   you can simply add the DistAlgo root directory to your `PYTHONPATH`
   environment variable by running the following command in your shell:

      export PYTHONPATH=<DAROOT>:${PYTHONPATH}

   Afterwards, the `da` module will be available in all `python` instances
   launched from this shell. You can add the above command to the
   initialization scripts for your shell to avoid typing this command in
   each new shell instance.

   The `<DAROOT>` directory installed using this method takes precedence
   over any DistAlgo packages installed by `pip` or `setup.py`.

### Instructions
#### How to Build: 
```
 python3.6 -m da.compiler <filename>
Run: python3.6 -m da -n <node name> <da file> <configuration file name>
	
In above command, replace <node name> with node process, <dafile> with da file containing main method and <configfilename> with config file name
```


### Running DistAlgo

RunSystem.da is the main file for running the whole distalgo project Byzantine chain replication project. The file RunSystem is run as “main” node. Example of commands
```
python3 -m da -n main RunSystem.da -i system.config 
```
* __-m :__ argument for providing the option to run Distalgo files.
* __-n :__ name of the node
* __RunSystem.da :__ name of the file
* __-i :__ parameter defines the config file(system.config) to pick while running the project.


#### Example:
Commands 1 to 6 are used for running a sample program using config file system.config

	1.) python3 -m da  --message-buffer-size 20000 -n onode  RunSystem.da -i ../config/ph3_9.wedge_extraop.config
				
	2.) python3 -m da --message-buffer-size 20000  -n client_0  -D RunSystem.da 
	3.) python3 -m da --message-buffer-size 20000  -n client_1 -D RunSystem.da 
	4.) python3 -m da --message-buffer-size 20000  -n replica_0 -D RunSystem.da  
	5.) python3 -m da --message-buffer-size 20000  -n replica_1  -D RunSystem.da 
	6.) python3 -m da --message-buffer-size 20000  -n replica_2 -D RunSystem.da 
	
	-i parameter helps to define the particular config file. It contains properties specific to retransmission, lik sleep time at replica, retransmission counter, client timeout specific to retransmission, which will trigger retransmission.

![alt text](olympus-final.gif)

#### Description:
	Config file = system.config
	t byzantine failure = 1
	client = 2
	replica = 3
	configuration_file_name = system.config 
* __NOTE:__ -D is specifically added to avoid that particular replica to run its Main


### Project Structure

* __“src”__ - contains files - RunSystem.da, Client.da, Olympus.da, Replica.da, config.py
* __“config”__ - contains configuration files, including test cases.
* __“logs”__ - contains log file
* __“pseudocode”__ - contains pseudocode from phase-1
* __ReadMe.md__
* __testing.txt__


### Pseudorandom Workload
We used python random module. Given 2 numbers (seed, n) where n is the total number of operations and seed is the initial seed number accepted by random module. The random number given by the random module is again seed back for generating the next random number. We made a pool of all the 4 operations [ get, append, slice, put]. The pool is configurable by any given number. The random number generated picks the operation from pool and generates a sequence of n operations.


### MultiHost 
Running the program on two host adityatomer and 'vagarwal'. Starting with the 'onode' on host adityatomer, listening on interfaces:

```
adityatomer> python3.6 -m da -H 0.0.0.0 -n onode RunSystem.da ../config/system.config

Starting 'replica_0', 'replica_1', 'replica_2' on host vagarwal, connecting the node on adityatomer  one by one

adityatomer$ python3.6 -m da  --message-buffer-size 20000 -H 172.24.225.182 -n onode RunSystem.da -i ../config/system.config
adityatomer$ python3 -m da  --message-buffer-size 20000 -H 172.24.225.182 -n client_0 -D RunSystem.da
adityatomer$ python3 -m da  --message-buffer-size 20000  -H 172.24.225.182 -n client_1 -D RunSystem.da
vagarwal$ python3 -m da --message-buffer-size 20000 -H 172.24.225.83 -R 172.24.225.182 -n replica_0 -D RunSystem.da
vagarwal$ python3 -m da --message-buffer-size 20000 -H 172.24.225.83 -R 172.24.225.182 -n replica_1 -D RunSystem.da
vagarwal$ python3 -m da --message-buffer-size 20000 -H 172.24.225.83 -R 172.24.225.182 -n replica_2 -D RunSystem.da
```
Starting 'client0' on host 'adityatomer', and connecting to the node on 'vagarwal'

adityatomer> python3 -m da -H 0.0.0.0 -R vagarwal -n client_0 -D RunSystem.da ../config/system.config


### Assumptions:
There wont be any kind of failures in failure scenarios itself. (failure scenarios should work as expected)



### Bugs and Limitations
 * In case of retransmission by a client. If all the replicas send the request to the head in this  case if the response is not found in cache. The head never sends the request from the cache.
 * In order to mock the retransmission, the tail replica sleeps for more time than the client timeout. The client send the retransmission request at all the replicas, the replica forward the request to head and head start the protocol from scratch, the retransmission request again timeout.
 * In case of multiple client, the verification of dictionary object at client side is not supported, Hence their can be concurrency issues.
 


