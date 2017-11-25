# iRacing Plugin for Prismatik
This plugin allows you to visualize data from iRacing with an ambilight.

## Installation
1. Install [Python 3](https://www.python.org/downloads/).
     * If you're using Windows, you'll need to [add Python to your system's 'PATH' environmental variable.](https://docs.python.org/using/windows.html#excursus-setting-environment-variables)
3. This plugin relies on the [pyirsdk library](https://github.com/kutu/pyirsdk). The module can be installed via [pip](https://pip.pypa.io/en/stable/quickstart/), which will also install [PyYAML](https://pypi.python.org/pypi/PyYAML).
```bash
 $ pip install pyirsdk
```
4. [Download the plugin](../../archive/master.zip) and unzip it. Place the folder into your `Prismatik\Plugins` directory, located in your user folder. Make sure the folder is named "Prismatik-iRacing" and does not have the branch on the end (e.g. "-master").
5. Open Prismatik and switch to the 'Plugins' page. At the top, click the "reload plugins" button and then click the checkbox to activate the iRacing plugin. If everything is set up properly the plugin status will switch to "(running)".

## License
This plugin is licensed under the terms of the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
