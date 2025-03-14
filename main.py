import time
import socket

import sentry_sdk
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.logger import logger as log
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, JWTDecodeError
from pydantic import ValidationError

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from tasks.celery_app import check_expiring_documents

from api import router
from core import configs
from ws import notification_manager
from ws.custom_websocket import CustomWebSocket


socket.setdefaulttimeout(15) # TODO: change to configs.SOCKET_TIMEOUT

app = FastAPI(
    title=configs.PROJECT_NAME,
    description=configs.DESCRIPTION,
    version=configs.VERSION,
    openapi_url=f"{configs.API_V1_PREFIX}/openapi.json",
    debug=configs.DEBUG,
)
scheduler = AsyncIOScheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: change to configs.ALLOWED_HOSTS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# sqlalchemy
# app.add_middleware(
#     DebugToolbarMiddleware,
#     panels=[
#         "debug_toolbar.panels.versions.VersionsPanel",
#         "debug_toolbar.panels.timer.TimerPanel",
#         "debug_toolbar.panels.settings.SettingsPanel",
#         "debug_toolbar.panels.headers.HeadersPanel",
#         "debug_toolbar.panels.request.RequestPanel",
#         "debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel",
#     ],
# )

app.include_router(router)

if configs.SENTRY_ENABLED:
    sentry_sdk.init(dsn=configs.SENTRY_DSN, traces_sample_rate=1.0)


@AuthJWT.load_config
def get_config():
    return configs


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    log.debug(f"Request: {request.method} {request.url} {request.client.host}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.json()})


@app.exception_handler(JWTDecodeError)
def jwt_decode_error_handler(request: Request, exc: JWTDecodeError):
    return JSONResponse(status_code=401, content={"detail": exc.message})


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: CustomWebSocket,
    user_id: str,
    token: str = Query(...),
    # Authorize: AuthJWT = Depends(),
):
    try:
        AuthJWT.jwt_required("websocket", token)
        if user_id is None:
            # raise AuthJWTException()
            return JSONResponse(status_code=400, content={"detail": "user_id is required"})
    except AuthJWTException:
        await websocket.close()
    custom_websocket = CustomWebSocket(websocket.scope, websocket.receive, websocket.send)
    await custom_websocket.accept()
    
    await notification_manager.connect(custom_websocket, user_id)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        notification_manager.disconnect(user_id, websocket)


@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(check_expiring_documents, CronTrigger.from_crontab('* * * * *'))
    scheduler.start()




