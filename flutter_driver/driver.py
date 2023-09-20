import base64
import json
from .command import *
from .jsonrpc import Server
from pywinauto.keyboard import *
from pywinauto.mouse import *

class FlutterDriver:
    _instance = None

    def __new__(cls, observatory_url):
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
    
    async def get_element_count(self, finder):
        command = GetElementCountCommand(self, finder, self.isolate_id)
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

    '''
    点击鼠标左键
    '''
    async def click(self, button = 'left', coords=(0, 0)):
        click(button, coords)
    
    '''
    点击鼠标右键
    '''
    async def right_click(self, coords=(0, 0)):
        right_click(coords)

    '''
    双击鼠标
    '''
    async def double_click(self, button = 'left', coords=(0, 0)):
        double_click(button, coords)

    '''
    长按鼠标
    '''
    async def long_press(self, button = 'left', coords=(0, 0)):
        press(button, coords)

    '''
    释放鼠标
    '''
    async def release(self, button = 'left', coords=(0, 0)):
        release(button, coords)
    
    '''
    滚动鼠标滚轮
    '''
    async def scroll(self, coords=(0, 0), wheel_dist=1):
        scroll(coords, wheel_dist)

    '''
    点击鼠标中键
    '''
    async def wheel_click(self, coords=(0, 0)):
        wheel_click(coords)

    """
    调用send_keys方法自动键入键或单个键操作（即按住，释放）到活动窗口。
    您可以使用任何Unicode字符（在Windows上）和下面列出的一些特殊键。 该模块也可在Linux上使用。
    可用的按键代码:
    {SCROLLLOCK}, {VK_SPACE}, {VK_LSHIFT}, {VK_PAUSE}, {VK_MODECHANGE},
    {BACK}, {VK_HOME}, {F23}, {F22}, {F21}, {F20}, {VK_HANGEUL}, {VK_KANJI},
    {VK_RIGHT}, {BS}, {HOME}, {VK_F4}, {VK_ACCEPT}, {VK_F18}, {VK_SNAPSHOT},
    {VK_PA1}, {VK_NONAME}, {VK_LCONTROL}, {ZOOM}, {VK_ATTN}, {VK_F10}, {VK_F22},
    {VK_F23}, {VK_F20}, {VK_F21}, {VK_SCROLL}, {TAB}, {VK_F11}, {VK_END},
    {LEFT}, {VK_UP}, {NUMLOCK}, {VK_APPS}, {PGUP}, {VK_F8}, {VK_CONTROL},
    {VK_LEFT}, {PRTSC}, {VK_NUMPAD4}, {CAPSLOCK}, {VK_CONVERT}, {VK_PROCESSKEY},
    {ENTER}, {VK_SEPARATOR}, {VK_RWIN}, {VK_LMENU}, {VK_NEXT}, {F1}, {F2},
    {F3}, {F4}, {F5}, {F6}, {F7}, {F8}, {F9}, {VK_ADD}, {VK_RCONTROL},
    {VK_RETURN}, {BREAK}, {VK_NUMPAD9}, {VK_NUMPAD8}, {RWIN}, {VK_KANA},
    {PGDN}, {VK_NUMPAD3}, {DEL}, {VK_NUMPAD1}, {VK_NUMPAD0}, {VK_NUMPAD7},
    {VK_NUMPAD6}, {VK_NUMPAD5}, {DELETE}, {VK_PRIOR}, {VK_SUBTRACT}, {HELP},
    {VK_PRINT}, {VK_BACK}, {CAP}, {VK_RBUTTON}, {VK_RSHIFT}, {VK_LWIN}, {DOWN},
    {VK_HELP}, {VK_NONCONVERT}, {BACKSPACE}, {VK_SELECT}, {VK_TAB}, {VK_HANJA},
    {VK_NUMPAD2}, {INSERT}, {VK_F9}, {VK_DECIMAL}, {VK_FINAL}, {VK_EXSEL},
    {RMENU}, {VK_F3}, {VK_F2}, {VK_F1}, {VK_F7}, {VK_F6}, {VK_F5}, {VK_CRSEL},
    {VK_SHIFT}, {VK_EREOF}, {VK_CANCEL}, {VK_DELETE}, {VK_HANGUL}, {VK_MBUTTON},
    {VK_NUMLOCK}, {VK_CLEAR}, {END}, {VK_MENU}, {SPACE}, {BKSP}, {VK_INSERT},
    {F18}, {F19}, {ESC}, {VK_MULTIPLY}, {F12}, {F13}, {F10}, {F11}, {F16},
    {F17}, {F14}, {F15}, {F24}, {RIGHT}, {VK_F24}, {VK_CAPITAL}, {VK_LBUTTON},
    {VK_OEM_CLEAR}, {VK_ESCAPE}, {UP}, {VK_DIVIDE}, {INS}, {VK_JUNJA},
    {VK_F19}, {VK_EXECUTE}, {VK_PLAY}, {VK_RMENU}, {VK_F13}, {VK_F12}, {LWIN},
    {VK_DOWN}, {VK_F17}, {VK_F16}, {VK_F15}, {VK_F14} 
    修饰符:
    '+': {VK_SHIFT}
    '^': {VK_CONTROL}
    '%': {VK_MENU} a.k.a. Alt键
    示例如何使用修饰符:
    send_keys('^a^c') # 全选（Ctrl + A）并复制到剪贴板（Ctrl + C）
    send_keys('+{INS}') # 从剪贴板插入（Shift + Ins）
    send_keys('%{F4}') # 使用Alt + F4关闭活动窗口 
    可以为特殊键指定重复计数。 {ENTER 2}表示按两次Enter键。
    示例显示如何按住或释放键盘上的按键:
    send_keys("{VK_SHIFT down}"
            "pywinauto"
            "{VK_SHIFT up}") # to type PYWINAUTO
    send_keys("{h down}"
            "{e down}"
            "{h up}"
            "{e up}"
            "llo") # to type hello 
    使用花括号来转义修饰符并将保留符号键入为单个键:
    send_keys('{^}a{^}c{%}') # 键入字符串 "^a^c%" (不会按下Ctrl键)
    send_keys('{{}ENTER{}}') # 键入字符串“{ENTER}”而不按Enter键 
    """
    async def send_keys(self, key):
        send_keys(key)

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