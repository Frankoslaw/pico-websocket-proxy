#!/usr/bin/env python
import sys
import json
import itertools
import inspect
from inspect import getmembers, isfunction

sys.path.insert(1, './adamed-robot')

from robot import Robot, map


# Function signatures file generator
signatures = {}
function_calls = {}

for function in getmembers(Robot, isfunction):
    function_calls[ function[1] ] = function[0]
    args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(function[1])

    if defaults == None:
        signatures[function[0]] = dict(itertools.zip_longest(args, []))
    else:
        signatures[function[0]] = dict(reversed(list(itertools.zip_longest(
            list(reversed(args)),
            list(reversed(defaults)) 
        ))))

with open('signatures.json', 'w', encoding='utf-8') as f:
    json.dump(signatures, f, ensure_ascii=False, indent=4)


# Web socket server for turbowarp
import ipaddress
import asyncio
from websockets.server import serve

print("Server running :D")
robots = {}

async def echo(websocket):
    async for message in websocket:
        # TODO: Reduce nesting
        command = message.split(' ')[0]
        args = message.split(' ')[1:]

        match command:
            case "init":
                ip = args[0]

                try:
                    ipaddress.ip_address(ip) # This will yield the error
                except:
                    await websocket.send(f"Incorrect IPv4 format")
                else:
                    robots[ip] = Robot(ip)

                    await websocket.send(f"Robot {ip} initialised")

            case "get_commands":
                await websocket.send('\n'.join(["init"] + list(signatures.keys())))

            case _:
                if command in signatures:
                    # TODO: Command handler
                    robot_ip = args[0]
                    robot = robots[robot_ip]

                    function_calls[command](robot, *args[1:])

                    await websocket.send(
                        json.dumps(signatures[command], ensure_ascii=False, indent=4)
                    )
                else:
                    await websocket.send("This command does not exists")


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
