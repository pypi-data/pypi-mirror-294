import json
from . import ai, config, schemas, router

@router.post(config.API_PATH + "/chat/general")
def general_chat(
    data: schemas.ChatMessage,
    ):
    text = ai.completions(json.loads(data.prompt))
    return {
        "status": "success",
        "data": {
            "response": text,
        }
    }
