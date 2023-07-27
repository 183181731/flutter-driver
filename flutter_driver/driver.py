import base64
import json
from .command import *
from .jsonrpc import Server

class FlutterDriver:
    _instance = None

    def __new__(cls, observatory_url):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
            cls._instance.observatory_url = observatory_url if observatory_url.startswith('ws') else "ws://{}ws".format(observatory_url[7:])
            cls._instance.command_executor = None
            cls._instance.isolate_id = None
        return cls._instance        

    async def connect(self):
        """
        connect to flutter driver
        """
        if self.client is None:
            self.client = Server(self.observatory_url, timeout=10)
            await self.client.ws_connect()
            self.command_executor = CommandExecutor()
            await self.get_isolate_id()

    async def close(self):
        """close driver ws connect
        """
        if self.client:
            await self.client.close()

    async def get_isolate_id(self):
        """get main isolate id
        """
        command = GetVMCommand(self)
        await command.execute()
        self.isolate_id = command.isolate_id

    async def is_enable_driver(self):
        """ ext.flutter.driver is in extensionRPCs list  

        Returns:
            bool: enableFlutterDriverExtension is enable
        """
        command = GetIsolateInfoCommand(self, self.isolate_id)
        extensionRPCs =  await command.execute()
        return 'ext.flutter.driver' in extensionRPCs

    async def find_element(self, finder):
        """find element by FlutterFinder

        Args:
            finder (_type_): _description_

        Returns:
            _type_: _description_
        """
        command = FindElementCommand(self, finder, self.isolate_id)
        self.command_executor.add_command(command)
        await self.command_executor.execute_commands()
        return FlutterElement(self, finder)

    async def find_element_by_semantics_label(self, label, isRegExp=False, index=None):
        return await self.find_element(FlutterFinder().by_semantics_label(label, isRegExp, index))

    async def find_element_by_text(self, text, index=None):
        return await self.find_element(FlutterFinder().by_text(text, index))

    async def find_element_by_tooltip(self, tooltip, index=None):
        return await self.find_element(FlutterFinder().by_tooltip_message(tooltip, index))

    async def find_element_by_type(self, widget_type, index=None):
        return await self.find_element(FlutterFinder().by_type(widget_type, index))

    async def find_element_by_value_key(self, value, type='String', index=None):   # other type is int
        return await self.find_element(FlutterFinder().by_value_key(value, type, index))

    async def find_page_back(self):
        return await self.find_element(FlutterFinder().page_back())
    
    async def find_ancestor(self, of, matching, matchRoot=False, firstMatchOnly=False, index=None):
        return await self.find_element(FlutterFinder().by_ancestor(of, matching, matchRoot, firstMatchOnly, index))

    async def find_descendant(self, of, matching, matchRoot=False, firstMatchOnly=False, index=None):
        return await self.find_element(FlutterFinder().by_descendant(of, matching, matchRoot, firstMatchOnly, index))

    async def tap_element(self, finder):
        command = TapElementCommand(self, finder, self.isolate_id)
        self.command_executor.add_command(command)
        await self.command_executor.execute_commands()

    async def get_text(self, finder):
        command = GetElementTextCommand(self, finder, self.isolate_id)
        return await command.execute()

    async def enter_text(self, text):
        command = EnterTextCommand(self, text, self.isolate_id)
        self.command_executor.add_command(command)
        await self.command_executor.execute_commands()

    async def get_top_left(self, finder):
        command = GetOffsetCommand(self, finder, 'topLeft', self.isolate_id)
        return await command.execute()

    async def get_top_right(self, finder):
        command = GetOffsetCommand(self, finder, 'topRight', self.isolate_id)
        return await command.execute()
    
    async def get_bottom_left(self, finder):
        command = GetOffsetCommand(self, finder, 'bottomLeft', self.isolate_id)
        return await command.execute()
    
    async def get_bottom_right(self, finder):
        command = GetOffsetCommand(self, finder, 'bottomRight', self.isolate_id)
        return await command.execute()
    
    async def get_center(self, finder):
        command = GetOffsetCommand(self, finder, 'center', self.isolate_id)
        return await command.execute()

    async def screenshot(self, path):
        """get application screenshot(is not work for Web)

        Args:
            path (string): save image to .png path
        """
        command = GetScreenShotCommand(self)
        result = await command.execute()
        with open(path, "wb") as f:
            f.write(base64.b64decode(result))

    async def drag(self, start_x, start_y, offset_x, offset_y, duration):
        command = DragCommand(self, start_x, start_y, offset_x, offset_y, duration, self.isolate_id)
        self.command_executor.add_command(command)
        await self.command_executor.execute_commands()

class FlutterElement:
    def __init__(self, driver, finder):
        """_summary_

        Args:
            driver (FlutterDriver): driver for Flutter Application
            finder (FlutterFinder): finder for Element
        """
        self.driver = driver
        self.finder = finder

    async def click(self):
        """click element"""
        await self.driver.tap_element(self.finder)

    async def clear(self):
        """clean text in element"""
        await self.driver.enter_text('')

    async def get_text(self):
        """get element text

        Returns:
            string: Text on FlutterElement
        """
        return await self.driver.get_text(self.finder)
    
    async def get_location(self):
        """get element Location info

        Returns:
            { dx , dy }: return the element lefttop location
        """
        return await self.driver.get_top_left(self.finder)
    
    async def get_size(self):
        """get element size info

        Returns:
            { width, height }: return the element width and height
        """
        top_left = await self.driver.get_top_left(self.finder)
        bottom_right = await self.driver.get_bottom_right(self.finder)
        return {
            "width": bottom_right["dx"] - top_left["dx"],
            "height": bottom_right["dy"] - top_left["dy"]
        }

class FlutterFinder:
    def __init__(self):
        pass

    def by_semantics_label(self, label, isRegExp, index=None):
        finder = {
            "finderType":"BySemanticsLabel",
            "label": label,
            'isRegExp': isRegExp,
        }
        if (index!=None):
            finder.update({ "index": index })
        return finder

    def by_text(self, text, index=None):
        finder = {
            "finderType":"ByText",
            "text": text
        }
        if (index!=None):
            finder.update({ "index": index })
        return finder

    def by_tooltip_message(self, message, index=None):    
        finder = {
            "finderType":"ByTooltipMessage",
            "text": message
        }
        if (index!=None):
            finder.update({ "index": index })
        return finder
    

    def by_type(self, type, index=None):
        finder = {
            "finderType":"ByType",
            "type": type
        }
        if (index!=None):
            finder.update({ "index": index })
        return finder

    def by_value_key(self, value, type, index=None):
        finder = {
            "finderType":"ByValueKey",
            "keyValueString": value,
            "keyValueType": type,
        }
        if (index!=None):
            finder.update({ "index": index })
        return finder

    def by_ancestor(self, of, matching, matchRoot, firstMatchOnly, index=None):
        finder = {
            "finderType":"Ancestor",
            "of": json.dumps(of),
            "matching": json.dumps(matching),
            "matchRoot": matchRoot,
            "firstMatchOnly": firstMatchOnly
        }
        if (index!=None):
            finder.update({ "index": index })
        return finder

    def by_descendant(self, of, matching, matchRoot=False, firstMatchOnly=False, index=None):
        finder = {
            "finderType":"Descendant",
            "of": json.dumps(of),
            "matching": json.dumps(matching),
            "matchRoot": matchRoot,
            "firstMatchOnly": firstMatchOnly
        }
        if (index!=None):
            finder.update({ "index": index })
        return finder

    def page_back(self):
        return {
            "finderType":"PageBack"
        }

class CommandExecutor:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    async def execute_commands(self):        
        for command in self.commands:
            await command.execute()
        self.commands = []