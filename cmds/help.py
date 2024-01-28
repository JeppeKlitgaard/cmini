import os
import glob
from discord import Message
from importlib import import_module
from more_itertools import divide

from util import parser

WIDTH = 6
INDENT = '    '

def exec(message: Message):
    command = parser.get_arg(message)
    commands = sorted(x.replace('/', '.')[5:-3] for x in glob.glob('cmds/*.py'))
    
    if command:
        if not command in commands:
            return f"Unknown command `{command}`"

        mod = import_module(f'cmds.{command}')

        if hasattr(mod, 'use'):
            use = mod.use()
        else:
            use = f"{command} [args]"

        if hasattr(mod, 'desc'):
            desc = mod.desc()
        else:
            desc = "..."

        return (
            f'Help page for `{command}`:'
            f'```\n'
            f'{use}\n'
            f'{desc}\n'
            f'```'
        )

    else:
        cmds = []
        for cmd in commands:
            mod = import_module(f'cmds.{cmd}')

            if not all(hasattr(mod, x) for x in ['exec', 'desc', 'use']):
                continue

            cmds.append(cmd)

        lines = ['Usage: `!cmini (command) [args]`']
        lines.append('```')

        cols = divide(2, cmds)
        
        for row in zip(*cols):
            lines.append("".join(x.ljust(16) for x in row))

        lines.append('```')
        return '\n'.join(lines)