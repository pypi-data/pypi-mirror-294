from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xml_image_converter",
    version="0.0.14",
    author="jhmun",
    author_email="jhmun@miridih.com",
    description="python-node.js package sample lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miridih/xml-image-converter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        # 필요한 패키지를 여기에 나열
    ],
    entry_points={
        'console_scripts': [
            # 스크립트 진입점을 여기에 정의
            'run-node-script=Realtime_Rendering_Tool.my_module:run_node_script'
        ],
    },
    include_package_data=True,  # 이 옵션을 추가하여 패키지에 포함될 데이터를 명시
    package_data={
        # 'Realtime_Rendering_Tool': ['src/Realtime_Rendering_Tool/package.json'],
        '': ['bundle.mjs', 'package.json'],
    },
)