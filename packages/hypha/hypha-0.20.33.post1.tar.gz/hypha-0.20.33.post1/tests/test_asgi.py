"""Test ASGI services."""
from pathlib import Path

import pytest
import requests
from hypha_rpc.websocket_client import connect_to_server

from . import WS_SERVER_URL, SERVER_URL, find_item

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_asgi(fastapi_server, test_user_token):
    """Test the ASGI gateway apps."""
    api = await connect_to_server(
        {"name": "test client", "server_url": WS_SERVER_URL, "token": test_user_token}
    )
    workspace = api.config.workspace

    # Test app with custom template
    controller = await api.get_service("public/server-apps")

    source = (
        (Path(__file__).parent / "testASGIWebPythonPlugin.imjoy.html")
        .open(encoding="utf-8")
        .read()
    )
    config = await controller.launch(
        source=source,
        wait_for_service="hello-fastapi",
        timeout=30,
    )
    service = await api.get_service(f"{config.workspace}/hello-fastapi")
    assert "serve" in service

    response = requests.get(f"{SERVER_URL}/{workspace}/apps/hello-fastapi/")
    assert response.ok
    assert response.json()["message"] == "Hello World"

    await controller.stop(config.id)
    await api.disconnect()


async def test_functions(fastapi_server, test_user_token):
    """Test the functions service."""
    api = await connect_to_server(
        {"name": "test client", "server_url": WS_SERVER_URL, "token": test_user_token}
    )
    workspace = api.config["workspace"]
    token = await api.generate_token()

    # Test app with custom template
    controller = await api.get_service("public/server-apps")

    source = (
        (Path(__file__).parent / "testFunctionsPlugin.imjoy.html")
        .open(encoding="utf-8")
        .read()
    )
    config = await controller.launch(
        source=source,
        wait_for_service="hello-functions",
        timeout=30,
    )

    service = await api.get_service(f"{config.workspace}/hello-functions")
    assert "hello-world" in service

    response = requests.get(
        f"{SERVER_URL}/{workspace}/apps",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.ok
    cards = response.json()
    card = find_item(cards, "name", "FunctionsPlugin")
    svc = find_item(card["services"], "name", "hello-functions")
    assert svc

    response = requests.get(
        f"{SERVER_URL}/{workspace}/apps/hello-functions/hello-world",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.ok
    ret = response.json()
    assert ret["message"] == "Hello World"
    assert "user" in ret["context"]
    user_info = ret["context"]["user"]
    assert user_info["scope"]["workspaces"]["ws-user-user-1"] == "rw"

    response = requests.get(
        f"{SERVER_URL}/{workspace}/apps/hello-functions/hello-world/"
    )
    assert response.ok

    response = requests.get(
        f"{SERVER_URL}/{workspace}/apps/hello-functions/",
        headers={"origin": "http://localhost:3000"},
    )
    assert response.ok
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert response.content == b"Home page"

    response = requests.get(f"{SERVER_URL}/{workspace}/apps/hello-functions")
    assert response.ok
    assert response.content == b"Home page"

    await controller.stop(config.id)
    await api.disconnect()
