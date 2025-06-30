Spine-Asset-Py
==========
Spine Animation Asset Parser Library  
Spine 动画资源解析库

![PyPI - Version](https://img.shields.io/pypi/v/spine-asset?label=PyPI%20version)
![PyPI - Downloads](https://img.shields.io/pypi/dm/spine-asset?label=PyPI%20downloads)
[![GitHub Workflow - Test](https://img.shields.io/github/actions/workflow/status/isHarryh/Spine-Asset-Py/test.yml?label=Test)](https://github.com/isHarryh/Spine-Asset-Py/actions/workflows/test.yml)

## Introduction

This Python library implements [Spine](https://esotericsoftware.com) skeleton parsing.
Note that the library does not support rendering, as it is just designed for parsing purpose.

### Features

| Spine Version | Skeleton Binary Parsing | Skeleton JSON Parsing | Atlas Parsing |
| :------------ | :---------------------- | :-------------------- | :------------ |
| 3.8           | √ Yes                   | √ Yes                 | √ Yes         |

## Usage

### Installation

Install from PyPI:

```shell
pip install spine_asset
```

### Examples

The following code shows how to parse a binary skeleton file:

```py
from spine_asset.v38 import SkeletonBinary

path = "path/to/your/skeleton/file.skel"

with open(path, "rb") as f:
    skeleton_data = SkeletonBinary().read_skeleton_data(f.read())

print("This skeleton contains these animations:")
print([a.name for a in skeleton_data.animations])
```

If the skeleton file is in JSON format, just change all the `SkeletonBinary` to `SkeletonJSON`.

## Licensing

This project is licensed under the MIT License. See the [License](https://github.com/isHarryh/Spine-Asset-Py/blob/main/LICENSE) file for more details.
