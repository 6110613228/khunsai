from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import cv2 as cv
import numpy as np


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/index", response_class=HTMLResponse)
async def read_item(request: Request):
    value = 'Value'
    return templates.TemplateResponse("index.html", {"request": request, 'key': value, 'anotherKey': 'and it\'s value'})


@app.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_bytes()
            print('Got image')
            
            nparr = np.frombuffer(data, np.uint8)
            image = cv.imdecode(nparr, -1)
            #cv.imwrite('test.png', image)

            await websocket.send_text(f"got image")
        except WebSocketDisconnect:
            await websocket.close()
            print('Closed connection')
            break
