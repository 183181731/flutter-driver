import json
from jsonrpc_base import Request, TransportError
import uuid

class Command:
    def __init__(self, driver, isolate_id=None):
        self.driver = driver
        if isolate_id:
           self.isolate_id = isolate_id

    def build_command(self):
        pass

    async def execute(self):
        command = self.build_command()
        try:
            response = await self.driver.client.send_message(Request(method=command['method'], params=command['params'], msg_id=str(uuid.uuid4())))
            return self.parse_response(response)
        except TransportError as e:
            print(e)
            await self.driver.close()
            raise TransportError("command execute timeout")            

    def parse_response(self, response):
        pass

class GetVMCommand(Command):
    def build_command(self):
        return {'method': 'getVM', 'params': {}}

    def parse_response(self, response):
        self.isolate_id = response['isolates'][0]['id']

class GetIsolateInfoCommand(Command):
    def __init__(self, driver, isolate_id):
        super().__init__(driver, isolate_id)

    def build_command(self):
        return {
            'method': 'getIsolate', 
            'params': {
                'isolateId': self.isolate_id
            }
        }
    
    def parse_response(self, response):
        return response["extensionRPCs"]

class GetScreenShotCommand(Command):    
    def build_command(self):
        return {'method': '_flutter.screenshot', 'params': {}}
    
    def parse_response(self, response):
        return response['screenshot']

class FindElementCommand(Command):
    def __init__(self, driver, finder, isolate_id):
        super().__init__(driver, isolate_id)
        self.finder = finder

    def build_command(self):
        params = {
            'command': 'waitFor',
            'isolateId': self.isolate_id,
        }
        params.update(self.finder)
        return {
            'method': 'ext.flutter.driver',
            'params': params,
        }
    
    def parse_response(self, response):
        return response['response']
    
class GetOffsetCommand(Command):
    def __init__(self, driver, finder, offset_type, isolate_id):
        super().__init__(driver, isolate_id)
        self.finder = finder
        self.offset_type = offset_type

    def build_command(self):
        params = {
            'command': 'get_offset',
            'offsetType': self.offset_type,
            'isolateId': self.isolate_id,
        }
        params.update(self.finder)
        return {
            'method': 'ext.flutter.driver',
            'params': params,
        }
    
    def parse_response(self, response):
        return response['response']

class TapElementCommand(Command):
    def __init__(self, driver, finder, isolate_id):
        super().__init__(driver, isolate_id)
        self.finder = finder

    def build_command(self):
        params = {
            'command': 'tap',
            'isolateId': self.isolate_id,
        }
        params.update(self.finder)
        return {
            'method': 'ext.flutter.driver',
            'params': params,
        }

class EnterTextCommand(Command):
    def __init__(self, driver, text, isolate_id):
        super().__init__(driver, isolate_id)
        self.text = text

    def build_command(self):
        params = {
            'command': 'enter_text',
            'text': self.text,
            'isolateId': self.isolate_id,
        }
        return {
            'method': 'ext.flutter.driver',
            'params': params,
        }
    
class GetElementTextCommand(Command):
    def __init__(self, driver, finder, isolate_id):
        super().__init__(driver, isolate_id)
        self.finder = finder

    def build_command(self):
        params = {
            'command': 'get_text',
            'isolateId': self.isolate_id,
        }
        params.update(self.finder)
        return {
            'method': 'ext.flutter.driver',
            'params': params,
        }
    
    def parse_response(self, response):
        return response['response']['text']
    
class ScrollCommand(Command):
    def __init__(self, driver, finder, dx, dy, duration, frequency, isolate_id):
        super().__init__(driver, isolate_id)
        self.finder = finder
        self.duration = duration
        self.dx = dx
        self.dy = dy
        self.frequency = frequency

    def build_command(self):
        params = {
            'command': 'scroll',            
            'dx': self.dx,
            'dy': self.dy,
            'duration': self.duration,
            'frequency': self.frequency,
            'isolateId': self.isolate_id,
        }
        params.update(self.finder)
        return {
            'method': 'ext.flutter.driver',
            'params': params,
        }
    
    def parse_response(self, response):
        return response['response']