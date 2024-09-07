import typing
from .utils import SingletonMeta as SingletonMeta
from Server.FlowManager import Flow as Flow
from Server.server import HorusSocket as HorusSocket
from _typeshed import Incomplete

class Extensions(metaclass=SingletonMeta):
    socketio: Incomplete
    def __init__(self, socketio: typing.Optional['HorusSocket'] = None) -> None: ...
    def open(self, pluginID: str, pageID: str, data: typing.Optional[typing.Dict[str, typing.Any]] = None, title: str = 'Extension') -> None:
        """
        Opens the given extension (PluginPage) and passes the given data to it.

        :param pluginID: The ID of the plugin that contains the desired PluginPage (Extension).
        :param pageID: The ID of the PluginPage that represents the extension.
        :param data: The data to pass to the extension.
        """
    def storeExtensionResults(self, pluginID: str, pageID: str, data: typing.Optional[typing.Dict[str, typing.Any]] = None, title: str = 'Results') -> None:
        """
        Stores the results of the extension in the flow to be opened at any time.

        :param pluginID: The ID of the plugin that contains the desired PluginPage (Extension).
        :param pageID: The ID of the PluginPage that represents the extension.
        :param data: The results of the extension.
        :param title: The title of the results. This will be displayed on top of the block that produced the results.
        """
    def loadHTML(self, html: str, title: str, store: bool = True) -> None:
        """
        Loads the given HTML string into the extension.

        :param html: The HTML to load as a string.
        :param title: The title of the 'Result'.         This will be displayed on top of the block that produced the HTML.
        :param store: Whether to store the HTML as results or to open it inmediately.
        """
    def loadImage(self, image: str, title: str, store: bool = True) -> None:
        """
        Loads the given image into the extension.

        :param image: The path to the image to load. Supports png, jpg and gif.
        :param title: The title of the 'Result'.         This will be displayed on top of the block that produced the image.
        :param store: Whether to store the image as results or to open it inmediately.
        """
    def loadText(self, text: str, title: str, store: bool = True) -> None:
        """
        Loads the given text into the extension.

        :param text: The text to load.
        :param title: The title of the 'Result'.         This will be displayed on top of the block that produced the text.
        :param store: Whether to store the text as results or to open it inmediately.
        """
