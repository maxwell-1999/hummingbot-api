from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class BotAction(BaseModel):
    """Base class for bot actions"""

    bot_name: str = Field(description="Name of the bot instance to act upon")


class StartBotAction(BotAction):
    """Action to start a bot"""

    log_level: Optional[str] = Field(
        default=None, description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    script: Optional[str] = Field(
        default=None, description="Script name to run (without .py extension)"
    )
    conf: Optional[str] = Field(
        default=None, description="Configuration file name (without .yml extension)"
    )
    async_backend: bool = Field(
        default=False, description="Whether to run in async backend mode"
    )


class StopBotAction(BotAction):
    """Action to stop a bot"""

    skip_order_cancellation: bool = Field(
        default=False,
        description="Whether to skip cancelling open orders when stopping",
    )
    async_backend: bool = Field(
        default=False, description="Whether to run in async backend mode"
    )


class ImportStrategyAction(BotAction):
    """Action to import a strategy for a bot"""

    strategy: str = Field(description="Name of the strategy to import")


class ConfigureBotAction(BotAction):
    """Action to configure bot parameters"""

    params: dict = Field(description="Configuration parameters to update")


class ShortcutAction(BotAction):
    """Action to execute bot shortcuts"""

    params: list = Field(description="List of shortcut parameters")


class BotStatus(BaseModel):
    """Status information for a bot"""

    bot_name: str = Field(description="Bot name")
    status: str = Field(description="Bot status (running, stopped, etc.)")
    uptime: Optional[float] = Field(None, description="Bot uptime in seconds")
    performance: Optional[Dict[str, Any]] = Field(
        None, description="Performance metrics"
    )


class BotHistoryRequest(BaseModel):
    """Request for bot trading history"""

    bot_name: str = Field(description="Bot name")
    days: int = Field(default=0, description="Number of days of history (0 for all)")
    verbose: bool = Field(default=False, description="Include verbose information")
    precision: Optional[int] = Field(None, description="Decimal precision for numbers")
    timeout: float = Field(default=30.0, description="Request timeout in seconds")


class BotHistoryResponse(BaseModel):
    """Response for bot trading history"""

    bot_name: str = Field(description="Bot name")
    history: Dict[str, Any] = Field(description="Trading history data")
    status: str = Field(description="Response status")


class MQTTStatus(BaseModel):
    """MQTT connection status"""

    mqtt_connected: bool = Field(description="Whether MQTT is connected")
    discovered_bots: List[str] = Field(description="List of discovered bots")
    active_bots: List[str] = Field(description="List of active bots")
    broker_host: str = Field(description="MQTT broker host")
    broker_port: int = Field(description="MQTT broker port")
    broker_username: Optional[str] = Field(None, description="MQTT broker username")
    client_state: str = Field(description="MQTT client state")


class AllBotsStatusResponse(BaseModel):
    """Response for all bots status"""

    bots: List[BotStatus] = Field(description="List of bot statuses")


class StopAndArchiveRequest(BaseModel):
    """Request for stopping and archiving a bot"""

    skip_order_cancellation: bool = Field(
        default=True, description="Skip order cancellation"
    )
    async_backend: bool = Field(default=True, description="Use async backend")
    archive_locally: bool = Field(default=True, description="Archive locally")
    s3_bucket: Optional[str] = Field(None, description="S3 bucket for archiving")
    timeout: float = Field(default=30.0, description="Operation timeout")


class StopAndArchiveResponse(BaseModel):
    """Response for stop and archive operation"""

    status: str = Field(description="Operation status")
    message: str = Field(description="Status message")
    details: Dict[str, Any] = Field(description="Operation details")


# Bot deployment models
class V2ScriptDeployment(BaseModel):
    """Configuration for deploying a bot with a script"""

    instance_name: str = Field(description="Unique name for the bot instance")
    credentials_profile: str = Field(
        description="Name of the credentials profile to use"
    )
    image: str = Field(
        default="supurr/algotrade:0.1",
        description="Docker image for the Hummingbot instance",
    )
    script: Optional[str] = Field(
        default=None, description="Name of the script to run (without .py extension)"
    )
    script_config: Optional[str] = Field(
        default=None,
        description="Name of the script configuration file (without .yml extension)",
    )
    headless: bool = Field(default=False, description="Run in headless mode (no UI)")


class V2ControllerDeployment(BaseModel):
    """Configuration for deploying a bot with controllers"""

    instance_name: str = Field(description="Unique name for the bot instance")
    credentials_profile: str = Field(
        description="Name of the credentials profile to use"
    )
    controllers_config: List[str] = Field(
        description="List of controller configuration files to use (without .yml extension)"
    )
    max_global_drawdown_quote: Optional[float] = Field(
        default=None,
        description="Maximum allowed global drawdown in quote usually USDT",
    )
    max_controller_drawdown_quote: Optional[float] = Field(
        default=None,
        description="Maximum allowed per-controller drawdown in quote usually USDT",
    )
    image: str = Field(
        default="supurr/algotrade:0.1",
        description="Docker image for the Hummingbot instance",
    )
    headless: bool = Field(default=False, description="Run in headless mode (no UI)")
