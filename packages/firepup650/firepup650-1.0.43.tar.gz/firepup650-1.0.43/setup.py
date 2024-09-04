# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['firepup650']

package_data = \
{'': ['*']}

install_requires = \
['fkeycapture>=1.2.7,<2.0.0', 'fpsql>=1,<2,!=1.0.26']

setup_kwargs = {
    'name': 'firepup650',
    'version': '1.0.43',
    'description': 'Package containing various shorthand things I use, and a few imports I almost always use',
    'long_description': '# Firepup650\nPackage containing various shorthand things I use, and a few imports I almost always use\n### Change log:\n#### v.1.0.43:\nCalled the error the wrong thing\n#### v.1.0.42:\nSmall typo fix (`stackLevel` -> `stacklevel`)\n#### v.1.0.41:\nWindows "Support"\n#### v.1.0.40:\nAdd offset mapping all the way up to 10 Billion, which exceeds the integer limit.\n#### v.1.0.39:\nAdd offset mappings for exceeding 1 Million options, new limit is 10 Million options\n#### v.1.0.38:\nMappings for much larger menu sizes, hopefully no one should ever hit that limit.\n#### v.1.0.37:\nUpgrades to gp and gh, they now function as stand-alone prompts, and allow deletion of characters as well (`allowDelete` must be set to `True`)\n#### v.1.0.36:\nFix an old annoying bug with menus having an incorrect size calculation if the width of the menu was an even number\n#### v.1.0.35:\nAdds a few missing docstrings and fixes a bug with the menu function\n#### v.1.0.34:\nAdds methods to hide/show the cursor and a menu system\n#### v.1.0.33:\nFinally fixes `clear`\'s ascii option, and adds windows compatibility to the same\n#### v.1.0.32 (Breaking change!):\nBREAKING CHANGE: `input` -> `inputCast`\n\nAdds the `makeError` function, and fixes some mypy complaints\n#### v.1.0.31:\nAdds the `isMath` function provided by @python660 on Replit Ask\n#### v.1.0.30:\nFix all mypy stub issues\n#### v.1.0.29:\nProvide a mypy stub file\n#### v.1.0.28:\nUpdates `Color` to flush print by default.\n#### v.1.0.27:\nRenames many methods, old names are still avalible for backwards compatiblity however. Also, SQL was moved to it\'s own package entirely.\n#### v.1.0.26:\nAdds `remove_prefix` and `remove_suffix`, name mangles internal variables in `sql`, fixes a bug in `console.warn`, adds `__VERSION__`, `__NEW__`, and `__LICENSE__`, adds many aliases for `help()`.\n#### v.1.0.25:\nFix all bugs related to version `1.0.24`\'s patch.\n#### v.1.0.24:\nFixes a bug in `sql`\'s `addTable` function.\n#### v.1.0.23:\nAdds `sql` (class) and all it\'s functions\n#### v.1.0.22:\nAdds `flush_print`.\n#### v.1.0.21:\nAdds `bad_cast_message` to `input` and `replit_input`.\n#### v.1.0.20:\nFixes a bug where `replit_input` didn\'t cast to `cast`.\n#### v.1.0.19:\nUpdates `replit_input` to call (new) custom `input` that supports type casting under the hood.\n#### v.1.0.18:\nAdds Ease Of Use stuff to `bcolors`.\n#### v.1.0.17:\nAdds `cprint`.\n#### v.1.0.16:\nSame as `v.1.0.15`. Should be fixed now.\n#### v.1.0.15:\nSame as `v.1.0.14`, but I can\'t use the same number\n#### v.1.0.14:\nHopefully fixes poetry not showing certain project info.\n#### v.1.0.13:\nAdds `replit_input`\n#### v.1.0.12:\nDescription fix for `gp`, add `gh`.\n#### v.1.0.11:\nFix a bug in the `gp` method.\n#### v.1.0.10:\nAdd the `REPLIT` color to `bcolors`, and add `replit_cursor` to the module.\n#### v.1.0.9:\nSmall tweaks, nothing major.\n#### v.1.0.8:\nCat install collections. This better fix it.\n###### v.1.0.7:\nAdds `console` (class), `bcolors` (class), and `Color` (function). Fixes type hinting on various things (Lots of thanks to [@bigminiboss](https://pypi.org/user/bigminiboss/)!).\n#### v.1.0.6:\nHopefully, fixes an issue where the package doesn\'t install it\'s dependencies (Again. Hopefully.)\n#### v.1.0.5:\nHopefully, fixes an issue where the package doesn\'t install it\'s dependencies\n#### v.1.0.4:\nSubscript errors\n#### v.1.0.3:\nDependant errors\n#### v.1.0.2:\nRandom shorthand (literally)\n#### v.1.0.1:\nAdded animated typing function, sleep shorthand\n#### v.1.0.0:\nInitial Release!\n',
    'author': 'Firepup650',
    'author_email': 'firepyp650@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/F1repup650/firepup650-PYPI',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
