from fastapi import FastAPI, Request, Depends, HTTPException
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mqtt import FastMQTT, MQTTConfig
# import json
# import asyncio

from sqlalchemy.orm import Session
import logging

from api.app.statehandler import StateHandler

from powermon.dto.resultDTO import ResultDTO
from powermon.dto.deviceDTO import DeviceDTO
from powermon.dto.commandDTO import CommandDTO

from .db import crud, models, schemas
from .db.database import SessionLocal, engine

log = logging.getLogger("main")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

mqtt_config = MQTTConfig(host="localhost", port=1883, username="", password="")

mqtt = FastMQTT(config=mqtt_config)

mqtt.init_app(app)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_statehandler():
    handler = StateHandler()
    return handler


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    topic = "powermon/"
    # mqtt.client.subscribe(topic) #subscribing mqtt topic
    log.info(f"Connected: {client}, {flags}, {rc}, {properties}, {topic}")



@mqtt.subscribe("powermon/announce")
async def listen_to_announcements(client, topic, payload, qos, properties):
    handler = StateHandler()
    device = handler.recieved_announcement(payload.decode())
    print(f"Recieved announcement for {device.device_id}")
    mqtt.client.subscribe(f"powermon/{device.device_id}/results/#")

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    #print("Received message: ", topic, payload.decode(), qos, properties)
    handler = StateHandler()
    log.debug(F"Command result on topic {topic}")
    #if handler.is_command_result_topic(topic):
    handler.recieved_result(topic, payload)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


app.mount("/static", StaticFiles(directory="api/app/static"), name="static")

templates = Jinja2Templates(directory="api/app/templates")


@app.get("/")
def read_root(request: Request):
    handler = StateHandler()
    devices = handler.get_device_instances()
    print(devices)
    return templates.TemplateResponse("home.html.j2", {"request": request, "devices": devices})


@app.get("/messages/", response_model=list[schemas.MQTTMessage])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_mqtt_messages(db, skip=skip, limit=limit)
    return users


@app.get("/messages/{message_id}", response_model=schemas.MQTTMessage)
def read_message(message_id: int, db: Session = Depends(get_db)):
    mqtt_message = crud.get_mqtt_message(db, mqtt_message_id=message_id)
    if mqtt_message is None:
        raise HTTPException(status_code=404, detail="User not found")
    return mqtt_message


@app.get("/devices/{device_id}/runCommandCode/{command_code}", response_model=ResultDTO)
async def read_command(device_id: str, command_code: str, handler: StateHandler = Depends(get_statehandler)):  # noqa: F811
    result = None
    
    command_dto = CommandDTO.run_api_command(command_code=command_code, device_id=device_id)
    log.debug(f"Subcribing to {command_dto.result_topic}")
    mqtt.client.subscribe(command_dto.result_topic)
    await add_command(command_dto, handler=handler)

    result = await handler.get_next_result(command_dto.result_topic)

    return result

@app.post("/addCommand/", response_model=CommandDTO)
async def add_command(command_dto: CommandDTO, handler: StateHandler = Depends(get_statehandler)):
    log.debug("Add command")
    device = handler.get_device_instance(command_dto.device_id)
    if device is None:
        raise HTTPException(status_code=404, detail=f"Device id: {command_dto.device_id} not found")

    if command_dto.command_code not in device.port.protocol.commands.keys():
        raise HTTPException(
            status_code=404, 
            detail=f"Command: {command_dto.command_code} not found in protocol: {device.port.protocol.protocol_id}")

    mqtt.client.publish(f"powermon/{command_dto.device_id}/addcommand", command_dto.json())

    return command_dto


@app.get("/devices/", response_model=list[DeviceDTO])
def read_devices(handler: StateHandler = Depends(get_statehandler)):
    result = None

    result = handler.get_device_instances()

    return result


@app.get("/devices/{device_id}", response_model=DeviceDTO)
def read_device(device_id: str, handler: StateHandler = Depends(get_statehandler)):  # noqa: F811
    result = None

    result = handler.get_device_instance(device_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return result



@app.get("/results/", response_model=list[ResultDTO])
async def read_results(handler: StateHandler = Depends(get_statehandler)):
    result = None

    result = await handler.get_results()
    if result is None:
        raise HTTPException(status_code=404, detail="No command results found")

    return result
