# from .moudle1 import hello_world
from .Proxy_Pool import get_proxies
from .Proxy_Pool import check_proxy
from .Proxy_Pool import get_yourself_proxies


# 现在，你也可以在__init__.py中定义其他包级别的函数
def another_function():
    print("This is another function in the package.")

# 如果你还想导入整个module1模块，也可以这样做
# from . import module1

