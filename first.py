import asyncio
import json
import logging
import websockets
import time
import sys
import ssl
import pathlib
from pymata_express import pymata_express

logging.basicConfig()

GREEN_PIN = 2  # arduino pin number
RED_PIN = 3
A1 = 4
A2 = 5
AS = 6
B1 = 7
B2 = 8
BS = 9

# instantiate pymata_express
board = pymata_express.PymataExpress()

async def handler(websocket, path):
    await board.set_pin_mode_digital_output(GREEN_PIN)
    await board.set_pin_mode_digital_output(RED_PIN)
    await board.set_pin_mode_pwm_output(AS)
    await board.set_pin_mode_digital_output(A1)
    await board.set_pin_mode_digital_output(A2)
    await board.set_pin_mode_pwm_output(BS)
    await board.set_pin_mode_digital_output(B1)
    await board.set_pin_mode_digital_output(B2)
    # the data we are sending back and forth
    lightState = {"red": False, "green": False, 'x': 0, 'y': 0}
    if websocket:
        await websocket.send(json.dumps(lightState))
        async for message in websocket:
            lightState = json.loads(message)
            print(lightState)
            await stateHandler(lightState)
            await motorHandler(lightState)

async def stateHandler(lightState):
    await board.digital_write(RED_PIN, lightState["red"])
    await board.digital_write(GREEN_PIN, lightState["green"])

async def motorHandler(lightstate):
    x = float(lightstate["x"])
    y = float(lightstate["y"])
    SpeedL = int((y*255)+(x*255))
    SpeedR = int((y*255)+(-x*255))
    print(SpeedL, SpeedR)

    if x == 0 and y == 0:
        await board.pwm_write(AS, SpeedL)
        await board.digital_write(A1, 0)
        await board.digital_write(A2, 0)
        await board.pwm_write(BS, SpeedR)
        await board.digital_write(B1, 0)
        await board.digital_write(B2, 0)

    if SpeedL > 0:
        await board.pwm_write(AS, SpeedL)
        await board.digital_write(A1, 1)
        await board.digital_write(A2, 0)
    if SpeedL < 0:
        await board.pwm_write(AS, abs(SpeedL))
        await board.digital_write(A1, 0)
        await board.digital_write(A2, 1)

    if SpeedR > 0:
        await board.pwm_write(BS, SpeedR)
        await board.digital_write(B1, 1)
        await board.digital_write(B2, 0)
    if SpeedR < 0:
        await board.pwm_write(BS, abs(SpeedR))
        await board.digital_write(B1, 0)
        await board.digital_write(B2, 1)

#ssl_context = ssl.create_default_context()

'''
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("tankcontrol.local.crt")
ssl_context.load_cert_chain(localhost_pem)
'''

start_server = websockets.serve(handler, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()      
