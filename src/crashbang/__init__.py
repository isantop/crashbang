"""crashbang

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import argparse
import shlex
from typing import Dict, Tuple

from .command import CrashCommand

Result = Dict[int, bool]
Analysis = Tuple[int, int, int]

def runner(command:CrashCommand ,iterations:int) -> Result:
    print(f'Starting {iterations} iterations of program {command.program}...')
    results:Result = {}
    count:int = 1

    while count <= iterations:
        print(f'Starting run #{count} of {iterations}...')
        if command.run():
            results[count] = True
        else:
            results[count] = False
        count += 1
        print(f'Run #{count} complete!')

    return results

def analyze(results:Result) -> Analysis:
    successes:int = 0
    failures:int = 0
    total:int = 0

    for result in results.values():
        total += 1
        if result:
            successes += 1
        else:
            failures += 1

    return successes, failures, total

def output(command:CrashCommand, analysis:Analysis) -> str:
    success, fails, total = analysis
    try:
        fail_rate:float = fails / total
    except ZeroDivisionError:
        fail_rate:float = 0.0

    output:str = ''

    output += f'Program {command.program} test run of {total} runs completed. '
    output += 'Results:\n'
    output += f'  Total sucesses: {success}\n'
    output += f'  Total crashes: {fails}\n'
    output += f'  Failure rate: {fail_rate}'

    return output

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

def cli() -> int:
    """ The main CLI utility"""
    args = parse_args()
    command = CrashCommand()
    command.timeout = args.timeout
    command.program = args.program
    if args.arguments:
        command.arguments = shlex.split(args.arguments)
    
    print(f'Starting {args.iterations} iterations of program {command.program}...')
    results:Result = {}
    count:int = 1
    
    try:
        while count <= args.iterations:
            print(f'Starting run #{count} of {args.iterations}...')
            if command.run():
                results[count] = True
            else:
                results[count] = False
            count += 1
            print(f'Run #{count} complete!')

    except KeyboardInterrupt:
        print('\nExiting early because Ctrl-C was pressed')

    except Exception as e:
        print('ERROR: The test run could not be completed. Error details:')
        print(e)
        return 1

    analysis:Analysis = analyze(results)
    out:str = output(command, analysis)
    print(out)
    return 0