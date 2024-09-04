import os
from . import config, schemas, router


@router.get("/heartbeat")
def heartbeat():
    return {"status": "OK", "build": os.environ.get("COMMIT_HASH", "")}


@router.get(config.API_PATH + "/hello")
def hello_message():
    """
    This one is to show a GET method
    """
    return {
        "status": "success",
        "message": "hello world :)",
    }


@router.post(config.API_PATH + "/hello")
def hello_custom_message(
    data: schemas.HelloMessage=None,
    ):
    """
    This one is to show how schema check is done via pydantic
    """
    msg = data.message if data else "hello world :)"
    return {
        "status": "success",
        "message": msg,
    }
