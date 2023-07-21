#!/usr/bin/env python
import json
import itertools
import inspect
from inspect import getmembers, isfunction

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

with open('./static/signatures.json', 'w', encoding='utf-8') as f:
    json.dump(signatures, f, ensure_ascii=False, indent=4)


# Web socket server for turbowarp
import ipaddress
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://turbowarp.org"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

robots = {}
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        message = await websocket.receive_text()

        command = message.split(' ')[0]
        args = message.split(' ')[1:]

        match command:
            case "init":
                ip = args[0]

                try:
                    ipaddress.ip_address(ip)
                except:
                    await websocket.send_text(f"Incorrect IPv4 format")
                    continue

                robots[ip] = Robot(ip)
                await websocket.send_text(f"Robot {ip} initialised")
                continue
            case "get_commands":
                await websocket.send_text('\n'.join(["init"] + list(signatures.keys())))
                continue

        if command in signatures:
            robot_ip = args[0]
            robot = robots[robot_ip]

            function_calls[command](robot, *args[1:])

            await websocket.send(
                json.dumps(signatures[command], ensure_ascii=False, indent=4)
            )

            continue

        await websocket.send_text("This command does not exists")