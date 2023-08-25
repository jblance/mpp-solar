from fastapi import FastAPI, Request, Depends, HTTPException
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mqtt import FastMQTT, MQTTConfig
# import json
# import asyncio

from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .db.database import SessionLocal, engine
from .mqtthandler import MQTTHandler

from powermon.dto.resultDTO import ResultDTO
from powermon.dto.deviceDTO import DeviceDTO

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


def get_mqtthandler():
    handler = MQTTHandler()
    return handler


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    topic = "powermon/"
    # mqtt.client.subscribe(topic) #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties, topic)



@mqtt.subscribe("powermon/announce")
async def listen_to_announcements(client, topic, payload, qos, properties):
    handler = MQTTHandler()
    device = handler.recieved_announcement(payload.decode())
    for command in device.commands:
        print("Subscribing to command: ", command.result_topic)
        mqtt.client.subscribe(command.result_topic)
    
@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ", topic, payload.decode(), qos, properties)
    handler = MQTTHandler()
    if (handler.is_command_result_topic(topic)):
        print("Command result")
        result = ResultDTO.parse_raw(payload.decode())
        print(f"Result: {result}")
        handler.recieved_result(result)

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
    handler = MQTTHandler()
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


@app.get("/command/{command_code}", response_model=schemas.MQTTMessage)
async def read_command(command_code: str, handler: MQTTHandler = Depends(get_mqtthandler)):  # noqa: F811
    result = None

    result = await handler.register_command(command_code)

    return result


@app.get("/devices/", response_model=list[DeviceDTO])
def read_devices(handler: MQTTHandler = Depends(get_mqtthandler)):
    result = None

    result = handler.get_device_instances()

    return result


@app.get("/devices/{device_id}", response_model=DeviceDTO)
def read_device(device_id: str, handler: MQTTHandler = Depends(get_mqtthandler)):  # noqa: F811
    result = None

    result = handler.get_device_instance(device_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return result



@app.get("/results/", response_model=list[ResultDTO])
async def read_results(handler: MQTTHandler = Depends(get_mqtthandler)):
    result = None

    result = await handler.get_results()
    if result is None:
        raise HTTPException(status_code=404, detail="No command results found")

    return result
