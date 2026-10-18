import asyncio
import json

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from watchfiles import awatch

CONFIG_PATH = "./config.json"
config = {}

def load_config():
  global config

  with open(CONFIG_PATH) as file:
    try:
      newConfig = json.load(file)
    except:
      print("error parsing config")
      return

  config = newConfig

async def watch_config():
    async for _ in awatch(CONFIG_PATH):
        load_config()
        print(config)


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("starting...")
    if not config:
        load_config()

    print(config)

    task = asyncio.create_task(watch_config())
    yield
    # Clean up background task on shutdown
    task.cancel()


app = FastAPI(lifespan=lifespan)

@app.get("/{path:path}")
async def redirect(path):
  target = config.get(path)
  if target is None:
    raise HTTPException(status_code=404, detail=f"No redirect configured for {path}")

  return RedirectResponse("https://" + target)
