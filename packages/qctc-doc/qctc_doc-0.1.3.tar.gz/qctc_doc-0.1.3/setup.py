from setuptools import find_packages, setup
from pathlib import Path
from magic_doc.libs.version import __version__


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    requires = []

    for line in lines:
        if "http" in line:
            pkg_name_without_url = line.split("@")[0].strip()
            requires.append(pkg_name_without_url)
        else:
            requires.append(line)

    return requires


if __name__ == "__main__":
    with Path(Path(__file__).parent,
              'README.md').open(encoding='utf-8') as file:
        long_description = file.read()
    setup(
        name="qctc_doc",  # 项目名
        version=__version__,  # 自动从tag中获取版本号
        packages=find_packages() + ["magic_doc.bin", "magic_doc.resources"],  # 包含所有的包
        package_data={
            "magic_doc.bin": ["**"],  # 包含magic_doc.bin目录下的所有文件
            "magic_doc.resources": ["**"],  # 包含magic_doc.resources目录下的所有文件
            "magic_doc.contrib.office.formula": ["**"],  # 包含magic_doc.contrib.office.formula目录下的所有文件
        },
        license='Apache 2.0',
        extras_require={
            "gpu": [
                "paddlepaddle-gpu==2.6.1",
                "paddleocr==2.7.3", 
                "magic-pdf[full]==0.7.1",
            ],
            "cpu": [
                "paddlepaddle==3.0.0b1;platform_system=='Linux'",  # 解决linux的段异常问题
                "paddlepaddle==2.6.1;platform_system=='Windows' or platform_system=='Darwin'",  # windows版本3.0.0b1效率下降，需锁定2.6.1  
                "paddleocr==2.7.3", 
                "magic-pdf[full]==0.7.1",
            ],
        },
        description='A lightweight toolbox to manipulate documents',
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=parse_requirements("requirements.txt"),  # 项目依赖的第三方库
        url="https://github.com/QCTC-chain/magic-doc",
        python_requires=">=3.10, <3.11",  # 项目依赖的 Python 版本
        entry_points={
            "console_scripts": [
                "magic-doc=magic_doc.cli:cli_conv",
                "pdf2md=magic_doc.cli:pdf_cli"
            ],
        },
        include_package_data=True,
        zip_safe=False,  # 是否使用 zip 文件格式打包，一般设为 False
    )
