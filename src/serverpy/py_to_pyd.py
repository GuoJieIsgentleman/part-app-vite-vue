import setuptools
import Cython.Build
import distutils.core


def py_to_pyd(file):
    cpy = Cython.Build.cythonize(file)  # 返回distutils.extension.Extension对象列表

    distutils.core.setup(
        name='pyd的编译',  # 包名称
        version="1.0",    # 包版本号
        ext_modules=cpy,     # 扩展模块
        author="gj",  # 作者
        author_email="904009156@.qq.com"  # 作者邮箱
    )


if __name__ == '__main__':

    file = "server.py"  # 需要编译的文件
    py_to_pyd(file)
