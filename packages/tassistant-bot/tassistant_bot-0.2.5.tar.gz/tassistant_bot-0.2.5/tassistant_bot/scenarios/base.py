from typing import Optional
from abc import ABC, abstractmethod

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler


class BaseScenario(ABC, MessageHandler):
    """
    An abstract base class for handling scenarios in a Pyrogram client.

    This class extends `MessageHandler` and provides a framework for defining
    custom scenarios that involve handling messages.

    Overall this class is like a `MessageHandler` with custom states to handle

    :param filters: Message filters used to determine which messages the handler will respond to.
    :param state: Optional state parameter to maintain scenario-specific state information.
    """

    class Meta:
        """
        Metadata for the scenario.

        :var name: A string representing the name of the scenario.
        :var description: A string representing the description of the scenario.
        """

        name = "Name of Scenario"
        description = "Description of Scenario"

    def __init__(self, filters, state: Optional[dict] = None) -> None:
        """
        Initializes the BaseScenario instance.

        :param filters: Message filters used to determine which messages the handler will respond to.
        :param state: Optional state parameter to maintain scenario-specific state information.
        """
        super().__init__(self.handler, filters)
        self.state = state

    @abstractmethod
    async def configure(self, client: Client, message: Message) -> None:
        """
        Abstract method to configure the scenario.

        This method must be implemented by subclasses to define how the scenario should
        be configured based on the incoming message and client context.

        Getting args from message to store them etc.

        :param client: The Pyrogram client instance.
        :param message: The incoming message to configure the scenario for.
        """
        pass

    @abstractmethod
    async def init_all_handlers(self, client: Client) -> None:
        """
        Abstract method to initialize all handlers related to the scenario.

        This method must be implemented by subclasses to define how to set up additional
        handlers or processes needed for the scenario.

        :param client: The Pyrogram client instance.
        """
        pass

    async def post_configure(self, client: Client, message: Message) -> None:
        """
        Optionally override this method for additional processing after the scenario is configured.

        This method can be used to perform any actions needed after the scenario has been
        configured and handlers have been initialized.

        :param client: The Pyrogram client instance.
        :param message: The incoming message that triggered the scenario.
        """
        pass

    async def handler(self, client: Client, message: Message) -> None:
        """
        Handles the incoming message by configuring the scenario, initializing handlers,
        and performing post-configuration.

        :param client: The Pyrogram client instance.
        :param message: The incoming message to handle.
        """
        await self.configure(client, message)
        await self.init_all_handlers(client)
        await self.post_configure(client, message)
