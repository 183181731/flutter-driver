To use flutter-driver you will need to make a simple setup in your Flutter project.

At first, include flutter_driver package to your dev dependencies at pubspec.yaml:
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_driver:
    sdk: flutter
```
if you need more new command support, you can include flutter_driver from my version:
https://github.com/183181731/flutter_driver
clone and include it
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_driver:
    path: ../flutter_driver
```

Then go to your main.dart file and add enableFlutterDriverExtension() to your main function before runApp()
```dart
import 'package:flutter/material.dart';
import 'package:flutter_driver/driver_extension.dart';

void main() {
  enableFlutterDriverExtension();
  runApp(const MyApp());
}
```



# Getting the flutter-drvier

There are three ways to install and use the flutter-drvier.

1. Install from [PyPi](https://pypi.org), as ['flutter-drvier'](https://pypi.org/project/flutter-drvier/).

    ```shell
    pip install flutter-drvier
    ```

2. Install from source, via [PyPi](https://pypi.org). From ['flutter-drvier'](https://pypi.org/project/flutter-drvier/),
download and unarchive the source tarball (flutter-drvier-X.X.tar.gz).

    ```shell
    tar -xvf flutter-drvierr-X.X.tar.gz
    cd flutter-drvier-X.X
    python setup.py install
    ```

3. Install from source via [GitHub](https://github.com/183181731/flutter-drvier).

    ```shell
    git clone git@github.com:183181731/flutter-drvier.git
    cd flutter-drvier
    python setup.py install
    ```

# How to use

```python
import time
import asynctest

from flutter_driver import Runner
from flutter_driver import FlutterDriver

class FlutterAppTest(asynctest.TestCase):

    async def test_driver_for_windows(self):
        runner = Runner('Windows')
        vm_url = runner.runApp("E:\\FlutterProjects\\brushcore\\brush-v3\\flutter\\sample")
        driver = FlutterDriver(vm_url)
        time.sleep(10)
        await driver.connect()
        res = await driver.is_enable_driver()
        print(res)
        insertbtn = await driver.find_element_by_text("插入")   # 获取并点击插入菜单
        await insertbtn.click()
        time.sleep(1)

        xzbtn = await driver.find_element_by_text("形状")   # 获取并点击形状菜单
        await xzbtn.click()
        time.sleep(1)

        jxbtn = await driver.find_element_by_type('Image', index="24")   # 根据索引拿到具体某个形状的菜单
        await jxbtn.click()
        time.sleep(1)

        await driver.drag("781", "180", "300", "300", "500")   # 在画布的某个区域拖动绘制出图形
        
        time.sleep(20)
        # await driver.screenshot('screenshot.png')       # 获取屏幕截屏
        runner.stopApp()
        await driver.close()

if __name__ == '__main__':
    asynctest.main()
```

# How to get dartVM Observatory url

## run from flutter command

use flutter run:
```shell
flutter run -d [platform]
```
then you will see the dartVM Observatory url in the command:
```
An Observatory debugger and profiler on Chrome is available at: http://127.0.0.1:8293/YjBYCPqtkhc=
The Flutter DevTools debugger and profiler on Chrome is available at: http://127.0.0.1:9103?uri=http://127.0.0.1:8293/YjBYCPqtkhc=
```

## get form debug app

1. Windows

    use (await Service.getInfo()).serverUri.toString() to get observatoryUrl from 'dart:developer' packages

2. Web

      when run debug App in Web, you can see observatoryUrl output from devtool console

3. Android

    in Android observatoryUrl is output from logcat