from setuptools import setup, find_packages

setup(
    name='imgs2pdf',
    version='0.0.1',
    url='https://github.com/enkatsu/imgs2pdf',
    author='enkatsu',
    author_email='endkty0509@gmial.com',
    license='MIT',
    classifiers=[],
    keywords=['PDF', 'Image', 'Tool'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['Click', 'reportlab'],
    entry_points={
        'console_scripts': [
            'img2pdf = app:main'
        ]
    }
)
