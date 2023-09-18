from pywinauto.keyboard import *
import time

send_keys("{VK_LWIN}")
time.sleep(5)
send_keys("cmd")
send_keys("{VK_RETURN}")
#以上三行可以写成一行命令：send_keys("{VK_LWIN}cmd{VK_RETURN}")
time.sleep(10)
send_keys("python")
send_keys("{VK_RETURN}")