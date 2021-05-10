from setuptools import setup

version = '2.0.0'

setup(
    name='cleverbotfree',
    packages=['cleverbotfree'],
    version=version,
    description='Free Alternative For The Cleverbot API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='plasticuproject',
    author_email='plasticuproject@pm.me',
    url='https://github.com/plasticuproject/cleverbotfree',
    download_url='https://github.com/plasticuproject/cleverbotfree/archive/v' +
    version + '.tar.gz',
    keywords=['cleverbot', 'bot', 'api', 'free'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Chat', 'Topic :: Utilities'
    ],
    license='GPLv3',
    install_requires=['playwright', 'fake-useragent'],
    zip_safe=False,
    include_package_data=True)
