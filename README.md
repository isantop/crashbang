# crashbang
A tool to aid in testing the stability of programs.

Crashbang is a tool that allows you to easily run a program through several 
iterations, speeding up the process of testing a program's stability. It also 
gathers data about the iterations and can provide statistics about successful 
exits versus crashes. Data is presented upon test run completion and program 
output can be saved to a file for later analysis. There are also facilities for 
limited automated testing.

Crashbang is essentially a beefed up loop. It runs a program through the 
specified number of iterations and detects what status the program exited with. 
Non-zero exit status constitutes an error, so those are flagged as failures, 
while zero is counted as a success. If a timeout is specified and the program 
doesn't exit before the timeout is reached, crashbang will automatically close 
the program and the iteration is counted as a success. Crashbang can also detect 
crashed caused by a signal (e.g. SIGIOT, Segmentation faults, etc.) and will 
display the recieved signal in the output file. 

## Installation
The recommended way to install Crashbang is via `pip` from PyPi:

```
pip3 install crashbang
```

You can also install the program from git directly:
```
pip3 install git+https://github.com/isantop/crashbang
```

To install from a local copy of the git repository:
```
## From within the cloned git repo:
pip3 install .
```

## Usage
Basic usage is to prepend `crashbang` to the program you want to run. This will 
run through 10 iterations of the program, waiting for the program to naturally 
terminate before proceeding to the next one. 

```
crashbang program-name
```

### Adding Arguments
Arguments to pass to the tested program are specified using the -a flag, and 
must be wrapped in quotation marks.

```
crashbang program-name -a "--first-argument --second-argument=true"
```

### Options

#### Iterations
Crashbang supports any number of iterations. Iterations can be set using the 
`-i` flag. The default number of iterations is 10.

```
crashbang program-name -i 100
```

#### Timeout
A timeout can also be specified. This is helpful when creating large automated
testing runs. With the timeout specified, Crashbang waits for natural program 
termination up to the specified timeout. If the timeout is reached, the program 
is stopped and the iteration is counted as a success, then a new iteration is 
started. If the program exits with 0 prior to the timeout, the iteration is also 
considered successful. Crashes before the timeout are still treated as failures, 
and if the program exits for any reason before the timeout is reached, the 
remainder of the timeout is skipped and the next iteration begins immediately.

Timeouts can be specified in seconds with the '-t' flag:

```
crashbang program-name -t 10
```

## Output
Upon completion or termination of a test run, Crashbang will display the 
gathered statistics from the test run, including the program name, the total 
number of iterations, the number of successful iterations, the number of crashes 
detected, and the failure percentage. 

Crashbang currently handles the KeyboardInterrupt exception to allow it to 
display statistics for completed iterations if the user uses Ctrl-C to exit the 
test run early. The output will reflect the total number of completed iterations 
in addition to the successes and crashes. 

### Output File
Crashbang also outputs a file with the console output (stdout and stderr) of any 
failed iterations. It also outputs the iteration number and the exit status ( or 
signal, if the termination was caused by a signal). 


## Planned Features
The following features are currently not implemented, but are planned for 
inclusion:

* Performance/timing information
* Status and ETA for completion of a test run
* Expanded output control
* Hooks for other automated testing tools
