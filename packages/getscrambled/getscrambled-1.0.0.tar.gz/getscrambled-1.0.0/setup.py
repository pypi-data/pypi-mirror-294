# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getscrambled']

package_data = \
{'': ['*']}

install_requires = \
['stegano>=0.11.3,<0.12.0']

setup_kwargs = {
    'name': 'getscrambled',
    'version': '1.0.0',
    'description': 'Protect unintended copy of your images by hiding the key in plain sight',
    'long_description': '# GetScrambled ![python](https://img.shields.io/badge/python->=3.9_<3.13-blue)\n\n---\n\n## Description\n\nGetScrambled is a simple library that allows you to scramble a image. No key is needed to unscramble the image, because the key is stored in the image itself (steganography and least significant bit). The image is scrambled by shuffling blocks of pixels. The size of the blocks can be set by the user.\n\nThe library uses pillow for image manipulation.\n\n## Example\n\n```python\nfrom getscrambled.encode import encode\nfrom PIL import Image\n\n# Encode\nimage = Image.open("tests/data/baboon.png")\nscrambled_image = encode(image, block_size=16)\nscrambled_image.save("tests/artifacts/baboon_scrambled.png")\n\n# Decode\nfrom getscrambled.decode import decode\ndecoded_image = decode(scrambled_image)\ndecoded_image.save("tests/artifacts/baboon_decoded.png")\n```\n### Original and scrambled image\n![baboon](tests/data/baboon.png| width=100) ![baboon_scrambled](tests/artifacts/baboon_scrambled.png| width=100)\n\n## Installation\n\n```bash\npip install getscrambled\n```\n\n## Development and testing\n\n```bash\ngit clone https://github.com/Starmania/getscrambled\ncd getscrambled\npoetry install\npoetry run pytest\n```\n\n## Disclaimer ![warning](https://img.shields.io/badge/-warning-red)\n\nThis library is not meant to be used for security purposes nor to encrypt data. It will just make harder to see the original image. You could check that I never use the word "encrypt" in this repository.\n\n## Todo\n\n- [ ] More tests\n',
    'author': 'Starmania',
    'author_email': 'wycvhrt6vzscfpedxr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Starmania/getscrambled',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
