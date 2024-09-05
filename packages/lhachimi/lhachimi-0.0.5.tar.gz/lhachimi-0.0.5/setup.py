from setuptools import setup, find_packages
# pip install wheel
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload dist/*

VERSION = '0.0.5'
DESCRIPTION = 'A basic science package'

setup(
    name="lhachimi",
    version=VERSION,
    author="Mohamed Lhachimi",
    author_email="mohamedyoutu123@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy','matplotlib','sympy','scikit-learn'],
    keywords=['python', 'science', 'math', 'analysis', 'simplify science', 'programming'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
