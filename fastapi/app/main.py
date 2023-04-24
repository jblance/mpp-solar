from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mqtt import FastMQTT, MQTTConfig

from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

mqtt_config = MQTTConfig(
    host = "localhost",
    port = 1883,
    username = "",
    password = ""
)

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

receivedTopic = "test_topic"
receivedPayload = "test_payload"

def receivedTopic():
    return receivedTopic

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    topic = "mqtt"
    mqtt.client.subscribe(topic) #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties, topic)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    db = SessionLocal()
    crud.create_mqtt_message(db, schemas.MQTTMessage(id=1,topic=topic, message=payload.decode()))

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root():
    return {receivedTopic: receivedPayload}

@app.get("/messages/", response_model=list[schemas.MQTTMessage])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_mqtt_messages(db, skip=skip, limit=limit)
    return users


@app.get("/messages/{message_id}", response_model=schemas.MQTTMessage)
def read_message(message_id: int, db: Session = Depends(get_db)):
    
    db_user = crud.get_mqtt_message(db, mqtt_message_id=message_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

