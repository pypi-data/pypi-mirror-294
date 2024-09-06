from setuptools import setup, find_packages

setup(
    name="triangle_drawer_yx",  # 你的包名
    version="0.1.0",  # 版本号
    packages=find_packages(),  # 自动查找所有包
    install_requires=[
        "termcolor"  # 你的包所依赖的库
    ],
    author="Yuan Xin",  # 作者姓名
    author_email="yxskills46@gmail.com",  # 作者邮箱
    description="A package to draw colored triangles in console.",  # 包描述
    url="https://github.com/Skillsyx",  # 项目主页 (如果有)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 需要的Python版本
)
