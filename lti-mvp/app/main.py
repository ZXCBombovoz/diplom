from fastapi import FastAPI, Request, HTTPException
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.message_launch import MessageLaunch
from pylti1p3.oidc_login import OIDCLogin
from pylti1p3.exception import LtiException

app = FastAPI()

TOOL_CONFIG = ToolConfJsonFile("app/tool_conf.json")


@app.get("/")
def healthcheck():
    return {"status": "LTI MVP is running"}


@app.post("/lti/login")
async def lti_login(request: Request):
    try:
        oidc = OIDCLogin(request, TOOL_CONFIG)
        return oidc.redirect()
    except LtiException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/lti/launch")
async def lti_launch(request: Request):
    try:
        message_launch = MessageLaunch(request, TOOL_CONFIG)
        launch_data = message_launch.validate()

        user = launch_data.get_user()
        resource_link = launch_data.get_resource_link()

        return {
            "message": "LTI launch success",
            "user_id": user["sub"],
            "resource_link_id": resource_link["id"],
            "context_id": launch_data.get_context()["id"],
        }

    except LtiException as e:
        raise HTTPException(status_code=400, detail=str(e))

