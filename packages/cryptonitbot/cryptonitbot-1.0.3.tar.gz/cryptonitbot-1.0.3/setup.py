from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='cryptonitbot',
    version='1.0.3',
    description="A bot for encryption and decryption using Telegram",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="ruslanlap",
    author_email="your-email@example.com",
    url="https://github.com/ruslanlap/Cryptonit-BOT",
    packages=find_packages(),
    package_data={
        'cryptonit_bot': ['Instructions.txt'],
    },
    install_requires=[req.strip() for req in open('cryptonit_bot/requirements.txt')],
    entry_points={
        'console_scripts': [
            'cryptonitbot=cryptonit_bot.bot:run_bot',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
