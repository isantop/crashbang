"""crashbang

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import shlex
from typing import Dict, Tuple

from .command import CrashCommand
from . import helper

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
        print(f'Run #{count} complete!')
        count += 1

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
        fail_rate:float = fails / total * 100
    except ZeroDivisionError:
        fail_rate:float = 0.0

    output:str = ''

    output += f'Program {command.program} test run of {total} runs completed. '
    output += 'Results:\n'
    output += f'  Total sucesses: {success}\n'
    output += f'  Total crashes: {fails}\n'
    output += f'  Failure rate: {fail_rate}%'

    return output

def cli() -> int:
    """ The main CLI utility"""
    args = helper.parse_args()
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
            result = command.run()
            if result[0]:
                results[count] = True
            else:
                results[count] = False
                helper.save_error_output(result[1], count)
            print(f'Run #{count} complete!')
            count += 1

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