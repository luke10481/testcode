import os
import random
import subprocess

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


def open_chrome_with_profile(user_data_dir, profile_name, port=None):
    """
    使用特定用户配置打开Chrome，确保每个实例独立

    Args:
        user_data_dir: 用户数据目录路径
        profile_name: 配置文件名称
        port: 远程调试端口
    """
    chrome_options = Options()

    # 为每个配置文件创建独立的用户数据目录副本
    # 这样可以避免配置文件被同时访问的问题
    temp_user_data = os.path.join(os.path.dirname(user_data_dir),
                                  f"Temp_Chrome_Data_{profile_name.replace(' ', '_')}")

    # 复制配置文件到临时目录（如果需要保留历史数据）
    import shutil
    if not os.path.exists(temp_user_data):
        os.makedirs(temp_user_data, exist_ok=True)
        # 复制原有的配置文件
        source_profile = os.path.join(user_data_dir, profile_name)
        if os.path.exists(source_profile):
            shutil.copytree(source_profile,
                            os.path.join(temp_user_data, profile_name))

    # 添加必要的参数
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")

    # 使用临时用户数据目录
    chrome_options.add_argument(f"--user-data-dir={temp_user_data}")

    # 指定使用哪个配置文件
    chrome_options.add_argument(f"--profile-directory={profile_name}")

    #chrome_options.binary_location = r'C:\Users\59483\Documents\software\chrome\win64-144.0.7559.31\chrome-win64\chrome.exe'

    # 为每个实例分配不同的远程调试端口
    if port is None:
        port = random.randint(10000, 60000)
    chrome_options.add_argument(f"--remote-debugging-port={port}")

    # 禁用自动化控制特征
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # 添加更多稳定性参数
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-translate")
    #chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")

    # 设置driver路径
    driver_path = Service(r'C:\Users\59483\PycharmProjects\PythonProject1\chromedriver-win64\chromedriver.exe')

    try:
        # 创建驱动
        driver = webdriver.Chrome(service=driver_path, options=chrome_options)

        # 打开网页
        try:
            driver.get("https://www.baidu.com")
        except:
            pass

        return driver
    except Exception as e:
        print(f"创建Chrome实例时出错: {e}")
        # 清理临时目录
        if os.path.exists(temp_user_data):
            try:
                shutil.rmtree(temp_user_data)
            except:
                pass
        raise


# 清理Chrome残留进程的辅助函数
def kill_chrome_processes():
    """杀死所有Chrome相关进程"""
    try:
        # Windows系统
        subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        subprocess.call(['taskkill', '/F', '/IM', 'chromedriver.exe'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        time.sleep(2)
    except Exception as e:
        print(f"清理进程时出错: {e}")


if __name__ == "__main__":
    # 在开始前清理可能存在的Chrome进程
    kill_chrome_processes()

    # 默认用户数据目录路径
    import os

    default_user_data = os.path.join(os.environ['USERPROFILE'],
                                     'AppData', 'Local', 'Google', 'Chrome', 'User Data')

    drivers = []
    try:
        # 打开不同配置文件，使用不同的端口
        driver2 = open_chrome_with_profile(default_user_data, "Profile 1", 9222)
        drivers.append(driver2)
        time.sleep(3)  # 等待第一个实例完全启动

        driver3 = open_chrome_with_profile(default_user_data, "Profile 2", 9223)
        drivers.append(driver3)

        # 等待一段时间查看效果
        time.sleep(100)

    finally:
        # 使用完毕后关闭
        for driver in drivers:
            try:
                driver.quit()
            except:
                pass

        # 清理进程
        kill_chrome_processes()