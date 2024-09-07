from distutils.core import setup
from setuptools import find_packages
import re
import os

with open("README.md", "r") as f:
    long_description = f.read()

package_name = 'phpgoody'

dists = os.listdir('./dist')
print(dists)
latest_dist = sorted(dists)[-1]
# 正则找出最后的版本
latest_dist_version = re.search(r'^phpgoody-(\d+\.\d+\.\d+)', latest_dist).groups()[0]
# 最后的版本加一，如 1.0.2 -> 1.0.3
new_version = '.'.join([str(int(x) + 1) if i == 2 else x for i, x in enumerate(latest_dist_version.split('.'))])

# 删掉之前的dist
for dist in dists:
    os.remove(f'./dist/{dist}')

setup(
    name=package_name,
    version=new_version,
    description="Some useful php functions implemented by python.",
    long_description=long_description,
    author="Elevioux",
    author_email="elevioux@live.com",
    url="https://blog.gwlin.com",
    install_requires=["dateutils>=0.6"],
    license="MIT License",
    packages=find_packages(),
    platforms=["all"],
    python_requires=">=3.11",
)
