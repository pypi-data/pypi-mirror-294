from setuptools import setup, find_packages


def get_req(req_path):
    with open(req_path, encoding='utf8') as f:
        return f.read().splitlines()


INSTALL_REQ = get_req('requirements.txt')
setup(
    name='layoutDetr',
    version='0.0.1',
    install_requires=INSTALL_REQ,
    packages=find_packages(include=['*.pt', '*.pth']),
)
