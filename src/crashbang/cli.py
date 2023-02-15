"""crashbang

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

The CLI utility
"""

import shlex

from . import Result, Analysis, runner, analyze, output, parse_args
from .command import CrashCommand

def cli() -> int:
    """ The main CLI utility"""
    args = parse_args()
    command = CrashCommand()
    command.timeout = args.timeout
    command.program = args.program
    command.arguments = shlex.split(args.arguments)
    try:
        results:Result = runner(command, args.iterations)
    except Exception as e:
        print('ERROR: The test run could not be completed. Error details:')
        print(e)
        return 1
    analysis:Analysis = analyze(results)
    out:str = output(command, analysis)
    print(out)
    return 0
