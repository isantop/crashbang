"""crashbang

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Extra helper definitions and functions
"""

import argparse
from subprocess import CalledProcessError
from typing import Dict

# List of signals given by the linux kernel
# These are negative because subprocess returns negative values for return codes
# when a signal causes a process to error.
LINUX_SIGNALS:Dict[int, str] = {
    -1: 'SIGHUP',
    -2: 'SIGINT',
    -3: 'SIGQUIT',
    -4: 'SIGILL',
    -5: 'SIGTRAP',
    -6: 'SIGIOT',
    -7: 'SIGBUS',
    -8: 'SIGFPE',
    -9: 'SIGKILL',
    -10: 'SIGUSR1',
    -11: 'SIGSEGV',
    -12: 'SIGUSR2',
    -13: 'SIGPIPE',
    -14: 'SIGALRM',
    -15: 'SIGTERM',
    -16: 'SIGSTKFLT',
    -17: 'SIGCHLD',
    -18: 'SIGCONT',
    -19: 'SIGSTOP',
    -20: 'SIGTSTP',
    -21: 'SIGTTIN',
    -22: 'SIGTTOU',
    -23: 'SIGURG',
    -24: 'SIGXCPU',
    -25: 'SIGXFSZ',
    -26: 'SIGVTALRM',
    -27: 'SIGPROF',
    -28: 'SIGWINCH',
    -29: 'SIGIO',
    -30: 'SIGPWR',
    -31: 'SIGSYS',
}

# List of human-readable signals
# Used to look up the cause of an error when a process terminates.
LINUX_SIGNAL_EXP:Dict[str, str] = {
    'SIGABRT': 'Abort signal from abort(3)',
    'SIGALRM': 'Timer signal from alarm(2)',
    'SIGBUS': 'Bus error (bad memory access)',
    'SIGCHLD': 'Child stopped or terminated',
    'SIGCLD': 'A synonym for SIGCHLD',
    'SIGCONT': 'Continue if stopped',
    'SIGEMT': 'Emulator trap',
    'SIGFPE': 'Floating-point exception',
    'SIGHUP': 'Hangup detected on controlling terminal  or death of controlling process',
    'SIGILL': 'Illegal Instruction',
    'SIGINT': 'Interrupt from keyboard',
    'SIGIO': 'I/O now possible (4.2BSD)',
    'SIGIOT': 'IOT trap. A synonym for SIGABRT',
    'SIGKILL': 'Kill signal',
    'SIGLOST': 'File lock lost (unused)',
    'SIGPIPE': 'Broken pipe: write to pipe with no readers; see pipe(7)',
    'SIGPOLL': 'Pollable event (Sys V); synonym for SIGIO',
    'SIGPROF': 'Profiling timer expired',
    'SIGPWR': 'Power failure (System V)',
    'SIGQUIT': 'Quit from keyboard',
    'SIGSEGV': 'Invalid memory reference',
    'SIGSTKFLT': 'Stack fault on coprocessor (unused)',
    'SIGSTOP': 'Stop process',
    'SIGTSTP': 'Stop typed at terminal',
    'SIGSYS': 'Bad system call (SVr4);see also seccomp(2)',
    'SIGTERM': 'Termination signal',
    'SIGTRAP': 'Trace/breakpoint trap',
    'SIGTTIN': 'Terminal input for background process',
    'SIGTTOU': 'Terminal output for background process',
    'SIGUNUSED': 'Synonymous with SIGSYS',
    'SIGURG': 'Urgent condition on socket (4.2BSD)',
    'SIGUSR1': 'User-defined signal 1',
    'SIGUSR2': 'User-defined signal 2',
    'SIGVTALRM': 'Virtual alarm clock (4.2BSD)',
    'SIGXCPU': 'CPU time limit exceeded (4.2BSD); see setrlimit(2)',
    'SIGXFSZ': 'File size limit exceeded (4.2BSD); see setrlimit(2)',
    'SIGWINCH': 'Window resize signal (4.3BSD, Sun)',
}

def save_error_output(problem:CalledProcessError , iteration:int) -> None:
    stdout:str = problem.stdout.decode('UTF-8')
    stderr:str = problem.stderr.decode('UTF-8')
    returncode:int = problem.returncode

    output:str = f'Crashbang test run #{iteration}: FAIL: '

    if returncode < 0:
        signal_name:str = LINUX_SIGNALS[returncode]
        signal_meaning:str = LINUX_SIGNAL_EXP[signal_name]
        output += f'Program recieved signal {signal_name} - {signal_meaning}\n'
    else:
        output += f'exited with return code {returncode}\n'
    output += 'Command output below:\n\n'
    output += f'stdout:\n{stdout}\n\nstderr:\n{stderr}\n\n'
    with open('crashbang_output.txt', mode='a') as output_file:
        output_file.write(output)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='crashbang',
        description='A tool to aid in testing the stability of programs'
    )

    parser.add_argument(
        'program',
        help='The command line program to run.'
    )

    parser.add_argument(
        '-a',
        '--arguments',
        help='Arguments to pass to the command line program'
    )

    parser.add_argument(
        '-i',
        '--iterations',
        type=int,
        default=10,
        help='The number of iterations to run (Default: 10)'
    )

    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=0,
        help=(
            'A timeout (in seconds) to wait for before ending an iteration. If '
            'an iteration takes longer than this time to complete, it will be '
            'ended and the iteration will be counted as a success.'
        )
    )

    return parser.parse_args()