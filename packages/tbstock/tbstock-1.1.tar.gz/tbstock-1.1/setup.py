from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

# 定义包的一些属性
setup(
    name='tbstock',
    version='1.1',
    description='tanbao stock data analysis tools',
    author='tanbao',
    author_email='tanbao210@hotmail.com',
    url='',  # 假如你的这个包有个介绍网站或者github之类的，就可以写上
    # packages=find_packages(),  # 当包越来越多时，手动一个个添加维护成本太大了，可以借助setuptools提供的find_packages函数, 一次性递归地将起始目录下的所有模块包进来（有__init__.py才算是模块）
    python_requires='>=3.9, <3.10',
    # package_data={'':['*.so']},
    include_package_data=True,
    install_requires=[
        'typing_extensions',
        'pymysql',
        'akshare',
        'baostock',
        'loguru',
        'exchange_calendars',
        'tqdm',
        'pandas',
        'pyautogui',
        'selenium',
        'sqlalchemy',
        'pyecharts',
        'plottable',
        'snapshot_selenium',
        'TA-Lib',
        'backtrader',
    ],
    ext_modules=cythonize([
        "./tbstock/__init__.py",
        "./tbstock/dataAcquisition/__init__.py",
        "./tbstock/dataAcquisition/models.py",
        "./tbstock/dataAcquisition/saveDataToMysql.py",
        "./tbstock/dataAcquisition/stockDataCrawler.py",
        "./tbstock/dataBacktest/__init__.py",
        "./tbstock/dataBacktest/strategyBacktest.py",
        "./tbstock/dataManagement/__init__.py",
        "./tbstock/dataManagement/dataPreprocess.py",
        "./tbstock/dataRelease/__init__.py",
        "./tbstock/dataRelease/dataRelease.py",
        "./tbstock/tradeStrategy/__init__.py",
        "./tbstock/tradeStrategy/stockStrategy.py",
        "./tbstock/utils/__init__.py",
        "./tbstock/utils/utils.py",
    ]),
)
