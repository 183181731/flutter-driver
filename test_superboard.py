import time
import asynctest

from flutter_driver import Runner
from flutter_driver import FlutterDriver

class FlutterAppTest(asynctest.TestCase):

    async def test_driver_for_windows(self):
        # runner = Runner('Windows')
        # vm_url = runner.runApp("D:\\FlutterProjects\\brushcore\\brush-v3\\flutter\\sample")
        driver = FlutterDriver("http://127.0.0.1:58343/S6QPRxUpyY8=/")
        time.sleep(10)
        await driver.connect()
        res = await driver.is_enable_driver()
        print(res)
        insertbtn = await driver.find_element_by_text("文本框")   # 获取并点击插入菜单
        await insertbtn.click()
        time.sleep(1)

        await driver.drag("781", "180", "300", "300", "500")   # 在画布的某个区域拖动绘制出图形
        time.sleep(3)
        edtior = await driver.find_element_by_type('QuillEditor')
        await edtior.click()
        time.sleep(1)
        await driver.send_keys("哈哈哈哈")

        time.sleep(5)
        await driver.screenshot('screenshot.png')       # 获取屏幕截屏
        # runner.stopApp()
        await driver.close()

if __name__ == '__main__':
    asynctest.main()