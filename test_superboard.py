import time
import asynctest

from flutter_driver import Runner
from flutter_driver import FlutterDriver

class FlutterAppTest(asynctest.TestCase):

    async def test_driver_for_windows(self):
        runner = Runner('Web')
        vm_url = await runner.runApp("D:\\FlutterProjects\\brushcore\\brush-v3\\flutter\\sample")
        driver = FlutterDriver(vm_url)
        time.sleep(10)
        await driver.connect()
        res = await driver.is_enable_driver()
        print(res)
        insertbtn = await driver.find_element_by_text("画笔")   # 获取并点击插入菜单
        await insertbtn.click()
        time.sleep(1)
        await driver.drag("781", "180", "300", "300", "500")
        time.sleep(3)

        easer = await driver.find_element_by_text("橡皮擦")   
        await easer.click()
        time.sleep(1)
        await driver.drag("781", "180", "300", "300", "500")        
        time.sleep(5)
        # await driver.screenshot('screenshot.png')       # 获取屏幕截屏
        await runner.stopApp()
        await driver.close()

if __name__ == '__main__':
    asynctest.main()