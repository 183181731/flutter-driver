import asynctest
import time

from flutter_driver import FlutterDriver, FlutterFinder

class FlutterDriverTest(asynctest.TestCase):
    async def test_finders_for_windows(self):
        vm_url = "http://127.0.0.1:5322/nui91pl-Jss=/"
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