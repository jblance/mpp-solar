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

from powermon.dto.powermonDTO import PowermonDTO
from powermon.dto.scheduleDTO import ScheduleDTO
from powermon.dto.resultDTO import ResultDTO

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


@mqtt.subscribe("powermon/testmon/results/#")
async def listen_to_results(client, topic, payload, qos, properties):
    print("Received message for DB and long poll: ", topic, payload.decode(), qos, properties)
    # db = SessionLocal()
    # mqtt_message = crud.create_mqtt_message(db, schemas.MQTTMessage(id=1,topic=topic, message=payload.decode()))

    result = ResultDTO.parse_raw(payload.decode())
    print(f"Result: {result}")
    handler = MQTTHandler()
    handler.recieved_result(result)


@mqtt.subscribe("powermon/announce")
async def listen_to_announcements(client, topic, payload, qos, properties):
    handler = MQTTHandler()
    handler.recieved_announcement(payload.decode())


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
    devices = handler.get_powermon_instances()
    print(devices)
    return templates.TemplateResponse("home.html.j2", {"request": request, "schedules": devices})


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
async def read_message(command_code: str, handler: MQTTHandler = Depends(get_mqtthandler)):  # noqa: F811
    result = None

    result = await handler.register_command(command_code)

    return result


@app.get("/powermons/", response_model=list[PowermonDTO])
async def read_power_monitors(handler: MQTTHandler = Depends(get_mqtthandler)):
    result = None

    result = await handler.get_powermon_instances()

    return result


@app.get("/powermons/{powermon_name}", response_model=PowermonDTO)
async def read_power_monitors(powermon_name: str, handler: MQTTHandler = Depends(get_mqtthandler)):  # noqa: F811
    result = None

    result = await handler.get_powermon_instance(powermon_name)

    return result


@app.get("/powermons/{powermon_name}/schedules", response_model=list[ScheduleDTO])
async def read_schedules(powermon_name: str, handler: MQTTHandler = Depends(get_mqtthandler)):
    result = None

    result = await handler.get_powermon_instance(powermon_name)

    if result is None:
        raise HTTPException(status_code=404, detail="Powermon not found")
    return result.schedulesCommands


@app.get("/results/", response_model=list[ResultDTO])
async def read_results(handler: MQTTHandler = Depends(get_mqtthandler)):
    result = None

    result = await handler.get_results()
    if result is None:
        raise HTTPException(status_code=404, detail="No command results found")

    return result
