import subprocess
import re


class FlutterRunnerStrategy:
    def run_flutter_app(self):
        pass

    def get_dart_vm_url(self):
        pass

class Runner:

    def __init__(self, platform, path):
        if platform.system() == 'Windows':
            self.runner_strategy = WindowsFlutterRunnerStrategy(path)
        elif platform.system() == 'Darwin':
            self.runner_strategy = MacFlutterRunnerStrategy(path)
        elif platform.system() == 'Linux':
            self.runner_strategy = LinuxFlutterRunnerStrategy(path)
        elif platform.system() == 'Web':
            self.runner_strategy = WebFlutterRunnerStrategy(path)
        elif platform.system() == 'Android':
            self.runner_strategy = AndroidFlutterRunnerStrategy(path)
        elif platform.system() == 'iOS':
            self.runner_strategy = IOSFlutterRunnerStrategy(path)

    def runApp(self):
        self.runner_strategy.run_flutter_app()
        return self.runner_strategy.get_dart_vm_url()


class WindowsFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self):
        pass

    def run_flutter_app(self):
        cmd = 'flutter run -d windows'
        subprocess.Popen(cmd, shell=True)

    def get_dart_vm_url(self):
        output = subprocess.check_output('flutter run -v --machine', shell=True)
        output_str = output.decode('utf-8')
        pattern = re.compile(r'observatory-uri: (http://[^/]+:\d+/)')
        match = pattern.search(output_str)
        if match:
            return match.group(1)
        else:
            return None

class WebFlutterRunnerStrategy(FlutterRunnerStrategy):
    def __init__(self):
        pass

    def run_flutter_app(self):
        cmd = 'flutter run -d windows'
        subprocess.Popen(cmd, shell=True)

    def get_dart_vm_url(self):
        output = subprocess.check_output('flutter run -v --machine', shell=True)
        output_str = output.decode('utf-8')
        pattern = re.compile(r'observatory-uri: (http://[^/]+:\d+/)')
        match = pattern.search(output_str)
        if match:
            return match.group(1)
        else:
            return None
        
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