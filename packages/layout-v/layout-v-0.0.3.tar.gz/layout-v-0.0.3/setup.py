from setuptools import setup, find_packages


def get_req(req_path):
    with open(req_path, encoding='utf8') as f:
        return f.read().splitlines()


INSTALL_REQ = get_req('/home/najm/Downloads/LayoutDetr/layout_detector/requirements.txt')
setup(
    name='layout-v',
    version='0.0.3',
    install_requires=INSTALL_REQ,
    packages=find_packages(include=['*.pt', '*.pth']),
)
