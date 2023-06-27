from commons import *
import xor, feistel

modules = [xor, feistel]

def for_module(module, action):
    action(module)

def foreach_module(actions):
    for module in modules:
        for action in actions:
            for_module(module, action)

def exec(command: str, module):
    next_commands = ""
    commands = command.split(";")
    if len(commands) > 1:
        next_commands = ";".join(commands[1:])
        command = commands[0]
    command = command.lstrip(" ")
    command = command.rstrip(" ")
    tokens = command.split(" ")
    cmd = tokens[0]
    has_args = len(tokens) > 1
    
    module.exec(cmd, tokens, has_args)
    
    if next_commands:
        exec(next_commands, module)

inp = "-"

foreach_module([lambda module: module.print_menu(),
                lambda module: module.init()])

while inp != "":
    inp = input("> ")
    nl()
    try:
        if inp == "help":
            foreach_module([lambda module: module.print_menu()])
            continue

        foreach_module([lambda module: exec(inp, module)])
    except Exception as e:
        print("Помилка, спробуйте ще раз!")
        print(e)
