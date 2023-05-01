from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# New stuff
def create_mqtt_message(db: Session, mqtt_message: schemas.MQTTMessageCreate):
    db_mqtt_message = models.MQTTMessage(topic=mqtt_message.topic, message=mqtt_message.message)
    db.add(db_mqtt_message)
    db.commit()
    db.refresh(db_mqtt_message)
    return db_mqtt_message

def get_mqtt_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MQTTMessage).offset(skip).limit(limit).all()

def get_mqtt_message(db: Session, mqtt_message_id: int):
    return db.query(models.MQTTMessage).filter(models.MQTTMessage.id == mqtt_message_id).first()