import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    # handler = MQTTHandler()
    # devices = handler.get_powermon_instances()
    devices = "devices..."
    print(devices)
    return templates.TemplateResponse("home.html.j2", {"request": request, "schedules": devices})


if __name__ == "__main__":
    config = uvicorn.Config("api:app", host="0.0.0.0", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
