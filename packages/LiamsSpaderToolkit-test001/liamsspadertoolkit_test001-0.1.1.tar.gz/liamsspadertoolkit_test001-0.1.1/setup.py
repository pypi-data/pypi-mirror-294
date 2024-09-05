from setuptools import setup, find_packages

setup(
    name='LiamsSpaderToolkit_test001',
    version='0.1.1',
    packages=find_packages(),
    description='liam`s 自定义爬虫私人包.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Liam',
    author_email='a61628904@163.com',
    # url='https://github.com/your-username/your-package',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # install_requires=[
    #     'dependency1',
    #     'dependency2',
    # ],
)