import os
import time
from typing import Optional, List, Literal, Dict, Any
import requests
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.webdriver import WebDriver

from .helpers import delay, get_screenshot
from .logging_config import logger
from .requests_handler import MiddleLayerRequestsHandler
from .types import AppiumSessionConfig, AppiumHandler, Command, ExecuteResponse, GptDriverConfig, \
    ServerSessionInitConfig, ServerConfig


class GptDriver:

    def __init__(self,
                 api_key: str,
                 driver: Optional[WebDriver] = None,
                 platform: Optional[str] = None,
                 device_name: Optional[str] = "",
                 platform_version: Optional[str] = "",
                 server_url: Optional[str] = None,
                 ):
        """
        Creates an instance of the GptDriver class.

        Initializes the GptDriver instance with the given configuration. This includes:

        - Setting the API key used for authenticating requests to the GPT Driver server.
        - Configuring the WebDriver instance if provided or validating server configuration if no WebDriver is given.
        - Setting up the Appium session configuration, including constructing the server URL and integrating device settings.

        Args:
            api_key (str): The API key used to authenticate requests to the GPT Driver server.
            driver (Optional[WebDriver]): The WebDriver instance to be used for the Appium session. If not provided, the server configuration is used.
            platform (Optional[str]): The platform of the device to be used for the Appium session. Required if no WebDriver is provided.
            device_name (Optional[str]): The name of the device to be used for the Appium session.
            platform_version (Optional[str]): The version of the platform to be used for the Appium session.
            server_url (Optional[str]): Emulation server url.

        Raises:
            ValueError: If neither a WebDriver instance nor a valid server configuration is supplied.
        """
        config = GptDriverConfig(
            driver=driver,
            server_config=ServerConfig(
                url=server_url,
                device=ServerSessionInitConfig(
                    platform=platform,
                    device_name=device_name,
                    platform_version=platform_version
                )
            )
        )
        self._api_key = api_key
        self._gpt_driver_session_id: Optional[str] = None
        self._appium_session_config: Optional[AppiumSessionConfig] = None
        self._driver: Optional[WebDriver] = None
        self._middlelayer_requests = MiddleLayerRequestsHandler()

        self._initialize_driver(config)
        self._initialize_appium_config(config)
        self._start_session()

    def _initialize_driver(self, config: GptDriverConfig):
        if config.driver:
            self._driver = config.driver
        else:
            is_valid_server_config = config.server_config and config.server_config.device.platform
            if not is_valid_server_config:
                raise ValueError("Either provide a driver, or a platform config")

    def _initialize_appium_config(self, config: GptDriverConfig):
        default_port = int(os.getenv('APPIUM_PORT', 4723))
        default_host = os.getenv('APPIUM_HOST', '127.0.0.1')

        server_url = f'http://{default_host}:{default_port}'
        device = ServerSessionInitConfig()
        if config.server_config:
            server_url = config.server_config.url or server_url
            device = config.server_config.device or device

        self._appium_session_config = AppiumSessionConfig(
            server_url=server_url,
            platform=device.platform,
            device_name=device.device_name,
            platform_version=device.platform_version
        )

    def _build_driver(self) -> WebDriver:
        """
        Builds a WebDriver instance based on the Appium session configuration.

        Returns:
            WebDriver: The initialized Appium WebDriver instance.
        """

        platform = self._appium_session_config.platform

        if platform.lower() == "android":
            options = UiAutomator2Options()
        else:
            options = XCUITestOptions()

        # Set up the desired capabilities for Appium
        options.load_capabilities({
            'deviceName': self._appium_session_config.device_name,
            'platformVersion': self._appium_session_config.platform_version,
        })

        logger().info(">> Connecting to the Appium server...")
        return webdriver.Remote(
            command_executor=self._appium_session_config.server_url,
            options=options
        )

    def _start_session(self):
        """
        Starts a new GPTDriver session and initializes the Appium session.
        The session creation process is logged, and a link is provided to monitor the session's execution.

        Raises:
            ValueError: If the session cannot be started or the driver is not properly initialized.
        """

        if self._driver:
            capabilities = self._driver.capabilities
            platform = capabilities['platformName']
            platform_version = capabilities.get('platformVersion', self._appium_session_config.platform_version)
            device_name = self._appium_session_config.device_name or capabilities.get('deviceName')
            self._appium_session_config.platform = platform
            self._appium_session_config.platform_version = platform_version
            self._appium_session_config.device_name = device_name
        else:
            self._driver = self._build_driver()

        self._appium_session_config.id = self._driver.session_id

        self._create_gpt_driver_session()

        rect_response = self._driver.get_window_rect()
        self._appium_session_config.size = {
            "width": rect_response['width'],
            "height": rect_response['height'],
        }

        logger().info(f">> Session created. Monitor execution at: {self._get_session_link()}")

    def _create_gpt_driver_session(self):
        """
        Creates a new GPTDriver session on the remote server.
        """
        logger().info(">> Starting session...")

        gpt_driver_session_response = self._middlelayer_requests.post(
            f"create",
            json={
                "api_key": self._api_key,
                "appium_session_id": self._appium_session_config.id,
                "device_config": {
                    "platform": self._appium_session_config.platform,
                    "device": self._appium_session_config.device_name,
                    "os": self._appium_session_config.platform_version,
                },
            }
        )
        self._gpt_driver_session_id = gpt_driver_session_response.json()['sessionId']

    def _get_session_link(self) -> str:
        """
        Returns the URL for monitoring the session.

        Returns:
            str: The session monitoring URL.
        """
        return f"https://app.mobileboost.io/gpt-driver/sessions/{self._gpt_driver_session_id}"

    def set_session_status(self, status: Literal["failed", "success"]):
        """
        Stops the current GPTDriver session and update its state.

        This method sends a request to the GPT Driver server to stop the session and logs the session status as either "failed" or "success."

        Args:
            status (Literal["failed", "success"]): Indicates the outcome of the session.
                                                  Use "success" if the session completed as expected,
                                                  or "failed" if the session encountered an error or issue.

        Raises:
            ValueError: If the request to stop the session fails.
        """
        logger().info(">> Stopping session...")
        self._middlelayer_requests.post(
            f"{self._gpt_driver_session_id}/stop",
            json={"api_key": self._api_key, "status": status}
        )

        logger().info(">> Session stopped.")
        self._gpt_driver_session_id = None

    def execute(self, command: str, appium_handler: Optional[AppiumHandler] = None):
        """
        Executes a specified command within the WebDriver session, optionally using an Appium handler.

        If an `appiumHandler` is provided, it will be invoked with the WebDriver instance to perform
        the command-specific operations. After executing the handler, the executed commands get logged on the GPTDriver servers.
        If the handler execution fails or no handler is provided, the command gets executed by the GPTDriver using just natural language.

        Args:
            command (str): The natural language command to be executed by the GPTDriver.
            appium_handler (Optional[AppiumHandler]): An optional function that processes Appium-specific commands.
                                                     If provided, this handler is executed instead of calling the GPTDriver servers.

        Raises:
            Exception: If an error occurs during the execution of the Appium handler or while processing the command by the GPTDriver.
        """
        logger().info(f">> Executing command: {command}")

        try:
            if appium_handler:
                appium_handler(self._driver)
                screenshot = get_screenshot(self._driver)
                self._middlelayer_requests.post(
                    f"{self._gpt_driver_session_id}/log_code_execution",
                    json={
                        "api_key": self._api_key,
                        "base64_screenshot": screenshot,
                        "command": command,
                    }
                )
            else:
                self._gpt_handler(command)
        except Exception:
            self._gpt_handler(command)

    def assert_condition(self, assertion: str):
        """
        Asserts a single condition using the GPTDriver.

        This method sends an assertion request and verifies if the specified condition is met.
        If the assertion fails, an error is thrown.

        Args:
            assertion (str): The condition to be asserted.

        Raises:
            AssertionError: If the assertion fails.
        """
        logger().info(f">> Asserting: {assertion}")
        results = self.check_bulk([assertion])

        if not list(results.values())[0]:
            raise AssertionError(f"Failed assertion: {assertion}")

    def assert_bulk(self, assertions: List[str]):
        """
        Asserts multiple conditions using the GPTDriver.

        This method sends a bulk assertion request and verifies if all specified conditions are met.
        If any assertion fails, an error is thrown listing all failed assertions.

        Args:
            assertions (List[str]): An array of conditions to be asserted.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        logger().info(f">> Asserting: {assertions}")
        results = self.check_bulk(assertions)

        failed_assertions = [
            assertions[i] for i, success in enumerate(results.values()) if not success
        ]

        if failed_assertions:
            raise AssertionError(f"Failed assertions: {', '.join(failed_assertions)}")

    def check_bulk(self, conditions: List[str]) -> Dict[str, bool]:
        """
        Checks multiple conditions and returns their results using the GPTDriver.

        This method sends a bulk condition request and returns the results of the conditions.

        Args:
            conditions (List[str]): An array of conditions to be checked.

        Returns:
            Dict[str, bool]: A dictionary mapping each condition to a boolean indicating whether the condition was met.
        """
        logger().info(f">> Checking: {conditions}")
        screenshot = get_screenshot(self._driver)

        response = self._middlelayer_requests.post(
            f"{self._gpt_driver_session_id}/assert",
            json={
                "api_key": self._api_key,
                "base64_screenshot": screenshot,
                "assertions": conditions,
                "command": f"Assert: {conditions}",
            },
        )

        return response.json()['results']

    def extract(self, extractions: List[str]) -> Dict[str, Any]:
        """
        Extracts specified information using the GPTDriver.

        This method sends a request to perform data extraction based on the provided extraction criteria and returns the results of the extractions.

        Args:
            extractions (List[str]): An array of extraction criteria. Each criterion specifies what information
                                     should be extracted from the session.

        Returns:
            Dict[str, Any]: A dictionary mapping each extraction criterion to the extracted data. The structure of the returned data depends on the specifics of the extraction criteria.
        """
        logger().info(f">> Extracting: {extractions}")
        screenshot = get_screenshot(self._driver)

        response = self._middlelayer_requests.post(
            f"{self._gpt_driver_session_id}/extract",
            json={
                "api_key": self._api_key,
                "base64_screenshot": screenshot,
                "extractions": extractions,
                "command": f"Extract: {extractions}",
            }
        )

        return response.json()['results']

    def _gpt_handler(self, command: str):
        """
        Handles the execution of a command using GPTDriver.

        Args:
            command (str): The natural language command to be executed.
        """
        try:
            condition_succeeded = False

            while not condition_succeeded:
                screenshot = get_screenshot(self._driver)

                logger().info(">> Asking GPT Driver for next action...")
                response = self._middlelayer_requests.post(
                    f"{self._gpt_driver_session_id}/execute",
                    json={
                        "api_key": self._api_key,
                        "command": command,
                        "base64_screenshot": screenshot,
                    }
                )
                execute_status = response.json()['status']
                if execute_status == "failed":
                    raise Exception(response.json().get('commands', [{}])[0].get('data', 'Execution failed'))

                condition_succeeded = execute_status != "inProgress"
                execute_response = ExecuteResponse(**response.json())
                for cmd, gpt_cmd_description in zip(execute_response.commands, execute_response.gptCommands):
                    logger().info(f">> Performing action: {gpt_cmd_description}")
                    self._execute_command(cmd)

                if not condition_succeeded:
                    time.sleep(1.5)

        except Exception as e:
            self.set_session_status(status="failed")
            raise e

    def _execute_command(self, command: Command):
        """
        Executes a specific command using requests.

        Args:
            command (Command): The command to be executed.
        """
        first_action = command.data.get('actions', [])[0] if command.data else None
        if first_action and first_action.get('type') == "pause" and first_action.get('duration'):
            delay(first_action['duration'] * 1000)
        else:
            requests.request(
                method=command.method,
                url=command.url,
                json=command.data
            )
