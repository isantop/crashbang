"""crashbang

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Represents a command to run.
"""

import shlex
import subprocess

from typing import List, Tuple, Any

Result = Tuple[bool, Any]

class CrashCommand:
    """
    A class representing a command to test for crashes
    """

    def __init__(self) -> None:
        self._program:str = ''
        self._arguments:List[str] = []
        self.timeout:int = 0
    
    
    def run(self) -> Result:
        """Run an instance of the specified command"""
        if not self.program:
            raise ValueError('No command is specified')
        
        run_command:List[str] = [self.program]
        run_command += self.arguments
        
        try:
            if self.timeout:
                result = subprocess.run(
                    run_command, 
                    timeout=self.timeout, 
                    check=True,
                    capture_output=True
                )
            else:
                result = subprocess.run(
                    run_command,
                    check=True,
                    capture_output=True
                )
            return (True, result)
        
        except subprocess.CalledProcessError as e:
            return (False, e)
        
        except subprocess.TimeoutExpired as e:
            return (True, e)

    @property
    def command(self) -> str:
        """str: the full command to run"""
        return ''
    
    @command.setter
    def command(self, command:str) -> None:
        com_list: List[str] = shlex.split(command)
        self.command = com_list.pop(0)
        self.arguments = com_list.copy()

    @property
    def program(self) -> str:
        """str: the name of the program to run"""
        return self._program
    
    @program.setter
    def program(self, prog:str) -> None:
        self._program = prog

    @property
    def arguments(self) -> List[str]:
        """list(str): the arguments which need to be appended to run."""
        return []
    
    @arguments.setter
    def arguments(self, args:List[str]) -> None:
        self._arguments = args
