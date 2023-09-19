import asyncio
import subprocess
import re
class FlutterRunnerStrategy:
    def run_flutter_app(self):
        pass

    def get_dart_vm_url(self):
        pass

    def close_app(self):
        pass

class Runner:
    def __init__(self, platform):
        if platform == 'Windows':
            self.runner_strategy = WindowsFlutterRunnerStrategy()
        elif platform == 'Darwin':
            self.runner_strategy = MacFlutterRunnerStrategy()
        elif platform == 'Linux':
            self.runner_strategy = LinuxFlutterRunnerStrategy()
        elif platform == 'Web':
            self.runner_strategy = WebFlutterRunnerStrategy()
        elif platform == 'Android':
            self.runner_strategy = AndroidFlutterRunnerStrategy()
        elif platform == 'iOS':
            self.runner_strategy = IOSFlutterRunnerStrategy()

    async def runApp(self, path, port=8889):
        await self.runner_strategy.run_flutter_app(path, port)
        return await self.runner_strategy.get_dart_vm_url()

    async def stopApp(self):
        await self.runner_strategy.close_app()

class WindowsFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self):
        self.process = None

    async def run_flutter_app(self, path, port):
        self.process = await asyncio.create_subprocess_shell('cmd.exe', cwd=path, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('build project at ' + path)
        self.process.stdin.write(("flutter run --observatory-port " + str(port) +  " --disable-service-auth-codes -d windows" + "\n").encode('utf-8'))
        self.process.stdin.close()

    async def get_dart_vm_url(self):
        url = None
        while True:
            output = await self.process.stdout.readline()
            output = output.strip().decode(encoding='gbk', errors='ignore')
            # 提取URL
            if('Dart VM Service' in output):
                url_regex = r'A Dart VM Service on Windows is available at: (http://\S+)'
                match = re.search(url_regex, output)
                if match:
                    url = match.group(1)
                    print('build complete, get Dart VM Service at:' + url)
                    break        
        return url
        
    async def close_app(self):
        self.process.stdout.feed_eof()  # 关闭 StreamReader
        self.process.stderr.feed_eof()  # 关闭 StreamReader
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])


class WebFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self):
        self.process = None

    async def run_flutter_app(self, path, port):
        self.process = await asyncio.create_subprocess_shell('cmd.exe', cwd=path, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('build project at ' + path)
        self.process.stdin.write(("flutter run --observatory-port " + str(port) +  " --disable-service-auth-codes -d chrome" + "\n").encode('utf-8'))
        self.process.stdin.close()

    async def get_dart_vm_url(self):
        url = None
        while True:
            output = await self.process.stdout.readline()
            output = output.strip().decode(encoding='gbk', errors='ignore')
            # 提取URL
            if('Dart VM Service' in output):
                url_regex = r'A Dart VM Service on Chrome is available at: (http://\S+)'
                match = re.search(url_regex, output)
                if match:
                    url = match.group(1)
                    print('build complete, get Dart VM Service at:' + url)
                    break
        return url + '/'
    
    async def close_app(self):
        self.process.stdout.feed_eof()  # 关闭 StreamReader
        self.process.stderr.feed_eof()  # 关闭 StreamReader
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
        
class AndroidFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self, path):
        pass

    def run_flutter_app(self):
        pass

    def get_dart_vm_url(self):
        pass

class IOSFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self, path):
        pass

    def run_flutter_app(self):
        pass

    def get_dart_vm_url(self):
        pass

class MacFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self, path):
        pass

    def run_flutter_app(self):
        pass

    def get_dart_vm_url(self):
        pass

class LinuxFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self, path):
        pass

    def run_flutter_app(self):
        pass

    def get_dart_vm_url(self):
        pass