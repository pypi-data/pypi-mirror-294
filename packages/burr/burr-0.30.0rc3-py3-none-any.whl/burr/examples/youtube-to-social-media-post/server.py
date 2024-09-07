import contextlib
import logging

import fastapi
import uvicorn
from application import ApplicationState, build_application

from burr.core import Application

logger = logging.getLogger(__name__)

# define a global `burr_app` variable
burr_app: Application[ApplicationState] = None  # type: ignore


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    """Instantiate the Burr application on FastAPI startup."""
    # set value for the global `burr_app` variable
    global burr_app
    burr_app = build_application()
    yield


app = fastapi.FastAPI(lifespan=lifespan)


@app.get("/social_media_post", response_model=ApplicationState)
def social_media_post(youtube_url: str) -> ApplicationState:
    """Creates a completion for the chat message"""
    _, _, state = burr_app.run(halt_after=["generate_post"], inputs={"youtube_url": youtube_url})

    return state.data


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=7443, reload=True)
