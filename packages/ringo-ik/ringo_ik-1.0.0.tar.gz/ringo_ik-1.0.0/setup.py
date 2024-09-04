import platform, glob, ntpath, os
from setuptools import setup

# OS specifics
CUR_OS = platform.system()
SHAREDOBJ_TEMPLATE = {
    'Windows': "ringo_base.cp{py_ver}-win_amd64.pyd",
    'Linux': "ringo_base.cpython-{py_ver}*-x86_64-linux-gnu.so",
}

assert CUR_OS in ['Linux',
                  'Windows'], "Only Linux and Windows platforms are supported"

# Python version specifics
python_version_tuple = platform.python_version_tuple()
py_ver = int(f"{python_version_tuple[0]}{python_version_tuple[1]}")

ringo_so_list = glob.glob(
    os.path.join('./ringo', SHAREDOBJ_TEMPLATE[CUR_OS].format(py_ver=py_ver)))
assert len(ringo_so_list) == 1
ringo_object_name = ntpath.basename(ringo_so_list[0])

for file in glob.glob('./ringo/*.pyd') + glob.glob('./ringo/*.so'):
    if ntpath.basename(file) != ringo_object_name:
        os.remove(file)

if CUR_OS == 'Windows':
    ADDITIONAL_FILES = ['*.dll']
elif CUR_OS == 'Linux':
    ADDITIONAL_FILES = []

setup(
    name='ringo_ik',
    version='1.0.0',
    author='Nikolai Krivoshchapov',
    python_requires=f'=={python_version_tuple[0]}.{python_version_tuple[1]}.*',
    install_requires=[
        'numpy',
        'networkx',
    ],
    platforms=['Windows', 'Linux'],
    packages=['ringo'],
    package_data={
        'ringo': [
            '__init__.py', ringo_object_name, 'cpppart/*', 'pyutils/**/*',
            'pyutils/*', *ADDITIONAL_FILES
        ]
    })
