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

    def runApp(self, path):
        self.runner_strategy.run_flutter_app(path)
        return self.runner_strategy.get_dart_vm_url()

    def stopApp(self):
        self.runner_strategy.close_app()


class WindowsFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self):
        self.process = None

    def run_flutter_app(self, path):
        self.process = subprocess.Popen('cmd.exe', cwd=path, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('build project at ' + path)
        self.process.stdin.write(("flutter run -d windows" + "\n").encode('utf-8'))
        self.process.stdin.close()        

    def get_dart_vm_url(self):
        url = None
        while True:
            output = self.process.stdout.readline().strip().decode(encoding='gbk', errors='ignore')
            # 提取URL
            if('Dart VM Service' in output):
                url_regex = r'A Dart VM Service on Windows is available at: (http://\S+)'
                match = re.search(url_regex, output)
                if match:
                    url = match.group(1)
                    print('build complete, get Dart VM Service at:' + url)
                    break
        return url
        
    def close_app(self):
        self.process.stdout.close()
        self.process.stderr.close()
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
        self.process.returncode = 1

class WebFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self):
        self.process = None

    def run_flutter_app(self, path):
        self.process = subprocess.Popen('cmd.exe', cwd=path, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('build project at ' + path)
        self.process.stdin.write(("flutter run -d chrome" + "\n").encode('utf-8'))
        self.process.stdin.close()

    def get_dart_vm_url(self):
        url = None
        while True:
            output = self.process.stdout.readline().strip().decode(encoding='gbk', errors='ignore')
            # 提取URL
            if('Dart VM Service' in output):
                url_regex = r'A Dart VM Service on Chrome is available at: (http://\S+)'
                match = re.search(url_regex, output)
                if match:
                    url = match.group(1)
                    print('build complete, get Dart VM Service at:' + url)
                    break
        return url + '/'
    
    def close_app(self):
        self.process.stdout.close()
        self.process.stderr.close()
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
        self.process.returncode = 1
        
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