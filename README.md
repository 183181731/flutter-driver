To use flutter-driver you will need to make a simple setup in your Flutter project.

At first, include flutter_driver package to your dev dependencies at pubspec.yaml:
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_driver:
    sdk: flutter
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
import asynctest
import time

from flutter_driver import FlutterDriver, FlutterFinder

class FlutterDriverTest(asynctest.TestCase):
    async def test_finders_for_windows(self):
        vm_url = "http://127.0.0.1:5322/nui91pl-Jss=/"    # dartVM Observatory url 
        driver = FlutterDriver(vm_url)
        await driver.connect()

        print(await driver.is_enable_driver())       # 输出ext.flutter.driver启用状态

        textfield = await driver.find_element_by_type("TextField")   # 获取并点击文本框控件
        await textfield.click()
        time.sleep(1)
        await driver.enter_text("测试文本")                     # 输入测试文本
        time.sleep(1)

        gotobtn = await driver.find_element_by_text("Go to Counter Page")     # 获取进入统计页面按钮并点击
        location = await gotobtn.get_location()
        size = await gotobtn.get_size()
        print(location)         # 输出控件位置信息
        print(size)             # 输出控件大小信息
        await gotobtn.click()

        time.sleep(1)
        textlable = await driver.find_element_by_value_key('home_text')    # 获取从上一页获取的文本信息
        text = await textlable.get_text()
        assert "测试文本" in text      #  断言文本包含了测试文本

        count_btn = await driver.find_element_by_tooltip("Increment")     # 获取并点击计数按钮控件
        await count_btn.click()

        tooltip = FlutterFinder().by_tooltip_message('Increment')     
        icon = FlutterFinder().by_type('Icon')
        
        count_btn = await driver.find_descendant(tooltip, icon)      # 使用子节点的方式定位计数按钮控件
        await count_btn.click()

        count_btn = await driver.find_ancestor(icon, tooltip)      # 使用祖先节点的方式定位计数按钮控件
        await count_btn.click()        

        countlable = await driver.find_element_by_value_key('counter_value')   # 获取计数统计显示数值
        count = await countlable.get_text()
        assert count == '3'      # 断言计数按钮点击了3次
        time.sleep(2)
        await driver.screenshot('screenshot.png')       # 获取屏幕截屏

        back_btn = await driver.find_page_back()       # 获取并点击返回按钮
        await back_btn.click()

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