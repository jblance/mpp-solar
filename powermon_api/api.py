from argparse import ArgumentParser
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi_mqtt import FastMQTT, MQTTConfig

from mppsolar.version import __version__  # noqa: F401
from powermon import read_yaml_file

# Set-up logger
log = logging.getLogger("")
log.setLevel(logging.INFO)

# Initial some variables
templates = Jinja2Templates(directory="powermon_api/templates")
config = None
mqtt = None

# Create FastAPI app instance
app = FastAPI()
app.mount("/static", StaticFiles(directory="powermon_api/static"), name="static")


@app.get("/")
def read_root(request: Request):
    global config
    log.info(f"{config=}")
    return templates.TemplateResponse("home.html.j2", {"request": request, "config": config})


def main():
    """main entry point for powermon api"""
    global config, mqtt
    description = f"Power Device Monitoring Api, version: {__version__}"
    parser = ArgumentParser(description=description)

    parser.add_argument(
        "-C",
        "--configFile",
        type=str,
        help="Full location of yaml config file",
        default="./powermon-api.yaml",
    )
    args = parser.parse_args()

    # Build configuration from config file etc
    log.info("Using config file: %s", args.configFile)
    config = {"configFile": args.configFile}
    # build config with details from config file
    config.update(read_yaml_file(args.configFile))

    log.info(f"{config=}")
    # if "mqttbroker" in config:
    #     mqtt_config = MQTTConfig(
    #         host=config["mqttbroker"].get("name"),
    #         port=config["mqttbroker"].get("port"),
    #         keepalive=60,
    #         username=config["mqttbroker"].get("username"),
    #         password=config["mqttbroker"].get("password"),
    #     )
    #     try:
    #         mqtt = FastMQTT(config=mqtt_config)
    #         mqtt.init_app(app)
    #     except Exception:
    #         print("Unable to connect to mqttbroker")
    #         mqtt = None

    uvicornConfig = uvicorn.Config(
        "powermon_api.api:app",
        host=config["api"].get("host", "0.0.0.0"),
        port=config["api"].get("port", 5000),
        log_level=config["api"].get("log_level", "info"),
        reload=True,
    )
    server = uvicorn.Server(uvicornConfig)
    server.run()
