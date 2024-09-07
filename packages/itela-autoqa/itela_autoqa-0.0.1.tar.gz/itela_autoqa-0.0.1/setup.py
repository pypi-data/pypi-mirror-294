from setuptools import setup, find_packages

setup(
    name="itela-autoqa",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "itela-autoqa=itela_autoqa.cli:main",
        ],
    },
    install_requires=[
        "openai>=1.43.1,<1.44",
        "playwright>=1.46.0,<1.47",
        "uuid==1.30",
    ],
    author="Chamara Herath",
    author_email="chamara.herath@itelasoft.com",
    description="iTelaSoft AI QA Automation CLI Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://git.itelasoft.com.au/chamara.herath/itelasoft-autoqa-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
