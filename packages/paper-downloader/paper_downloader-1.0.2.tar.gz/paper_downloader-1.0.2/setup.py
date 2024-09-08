from setuptools import setup, find_packages

setup(
    name="paper-downloader",  # 库的名称
    version="1.0.2",                   # 版本
    description="Download, Merge, and Rename",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # 使用 Markdown 格式的 README
    author="Wei Deng",
    author_email="dw-dengwei@outlook.com",
    url="https://github.com/dw-dengwei/paper-down",  # 项目主页 (例如 GitHub)
    packages=find_packages(),            # 自动查找并包含项目中的所有包
    install_requires=[                   # 项目依赖
        "requests>=2.28.0",
        "tqdm>=4.64.0",
        "pypdf>=4.3.1",
        "prompt-toolkit>=3.0.39"
    ],
    python_requires=">=3.8",             # 指定需要的 Python 版本
    classifiers=[                        # 分类标记，帮助 PyPI 标记项目类型
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={                       # 命令行工具
        'console_scripts': [
            'pd=paper_down.main:main',
        ],
    },
)
