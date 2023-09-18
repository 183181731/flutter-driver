import time
import asynctest

from flutter_driver import Runner
from flutter_driver import FlutterDriver
from flutter_driver import FlutterFinder

class FlutterAppTest(asynctest.TestCase):

    async def test_driver_for_windows(self):
        # runner = Runner('Windows')
        # vm_url = runner.runApp("E:\\FlutterProjects\\brushcore\\brush-v3\\flutter\\sample")
        driver = FlutterDriver("http://127.0.0.1:53403/dp60s1aT2qw=/")
        time.sleep(10)
        await driver.connect()
        # res = await driver.is_enable_driver()
        # print(res)
        insertbtn = await driver.find_element_by_text("插入")   # 获取并点击插入菜单
        await insertbtn.click()
        time.sleep(1)

        xzbtn = await driver.find_element_by_text("形状")   # 获取并点击形状菜单
        await xzbtn.click()
        time.sleep(1)

        imgfinder = FlutterFinder().by_type("Image")
        count = await driver.get_element_count(imgfinder)   # 获取匹配的元素个数
        print(count)
        time.sleep(1)

        jxbtn = await driver.find_element_by_type('Image', index="24")   # 根据索引拿到具体某个形状的菜单
        await jxbtn.click()
        time.sleep(1)

        await driver.drag("781", "180", "300", "300", "500")   # 在画布的某个区域拖动绘制出图形
        
        time.sleep(10)
        await driver.screenshot('screenshot.png')       # 获取屏幕截屏
        # runner.stopApp()
        await driver.close()

if __name__ == '__main__':
    asynctest.main()