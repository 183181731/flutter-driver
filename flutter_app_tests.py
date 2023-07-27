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