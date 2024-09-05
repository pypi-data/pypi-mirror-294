from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from botrun_ask_folder.fast_api.router_botrun_ask_folder import router
from botrun_ask_folder.fast_api.drive_api import (
    drive_api_router,
)
from botrun_ask_folder.fast_api.storage_api import (
    storage_api_router,
)
from botrun_ask_folder.fast_api.queue_api import (
    queue_api_router,
)
from botrun_ask_folder.fast_api.router_linebot import (
    linebot_router,
)

app = FastAPI()
api_botrun = FastAPI()


api_botrun.include_router(router)
api_botrun.include_router(drive_api_router)
api_botrun.include_router(storage_api_router)
api_botrun.include_router(queue_api_router)
api_botrun.include_router(linebot_router)
app.mount("/api/botrun", api_botrun)

# Mount Chainlit app
mount_chainlit(app=app, target="my_cl_app.py", path="/botrun_chat")
