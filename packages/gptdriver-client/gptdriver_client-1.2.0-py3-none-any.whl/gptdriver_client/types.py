from typing import Optional, List, Any, Literal, Callable, Awaitable
from pydantic import BaseModel
from appium.webdriver.webdriver import WebDriver

class Command(BaseModel):
    method: Literal['GET', 'DELETE', 'POST']
    url: str
    data: Any


class ExecuteResponse(BaseModel):
    commands: List[Command]
    status: Literal['inProgress', 'success', 'failed']
    gptCommands: List[str]


class DeviceSize(BaseModel):
    width: int
    height: int

AppiumHandler = Callable[[WebDriver], Awaitable[Any]]
PlatformLiteral = Literal['iOS', 'Android', 'ios', 'android']

class AppiumSessionConfig(BaseModel):
    id: Optional[str] = None
    platform: Optional[PlatformLiteral] = None
    device_name: Optional[str] = None
    platform_version: Optional[str] = None
    size: Optional[DeviceSize] = None
    server_url: str

class ServerSessionInitConfig(BaseModel):
    platform: Optional[PlatformLiteral] = None
    device_name: Optional[str] = None
    platform_version: Optional[str] = None

class ServerConfig(BaseModel):
    url: Optional[str] = None
    device: Optional[ServerSessionInitConfig] = None

class GptDriverConfig(BaseModel):
    driver: Optional[WebDriver] = None
    server_config: Optional[ServerConfig] = None

    class Config:
        arbitrary_types_allowed = True
