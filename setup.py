from distutils.core import setup

with open('README.rst') as readme:
    with open('HISTORY.rst') as history:
        long_description = readme.read()

VERSION = '2.2.1'

setup(
    install_requires=['requests'],
    name='python-telegram-handler',
    version=VERSION,
    packages=['telegram_handler'],
    url='https://github.com/prettyirrelevant/python-telegram-handler',
    download_url='https://github.com/prettyirrelevant/python-telegram-handler/archive/v%s.zip' % VERSION,
    keywords=['telegram', 'logging', 'handler', 'bot'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Debuggers',
        'Topic :: System :: Logging'
    ],
    long_description=long_description,
    license='MIT License',
    author='prettyirrelevant',
    author_email='ienioladewumi@gmail.com',
    description='A python logging handler that sends logs via Telegram Bot Api.',
)
