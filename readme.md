# TurboWarp proxy

Webscoket <-> UDP <-> Custom PICO proxy

## Installation and usage

```
python3 install -r requirements.txt
uvicorn main:app --reload
```

## Example websocket requests

```
init 192.168.1.21
get_modules
get 192.168.1.21
```

## TurboWarp

Extension after running the proxy will be exposed on `http://localhost:8000/`, port CANNOT be changed, because turbowarp requires it to disable local sandbox.
