# iRacing Plugin for Prismatik - Build Instructions
If you'd like to work with the plugin's source, here are some instructions to help you along the way.

## Source Setup
The repository can be used as-is to run the plugin from source, assuming you have Python and the required dependencies installed.

### Python and Dependencies
1. Install [Python 3](https://www.python.org/downloads/). This plugin was written with Python 3.6.
     * If you're using Windows, you'll need to [add Python to your system's 'PATH' environmental variable.](https://docs.python.org/using/windows.html#excursus-setting-environment-variables) Be sure to include the scripts directory as well in order to use modules from the command line.
2. This plugin relies on the [pyirsdk library](https://github.com/kutu/pyirsdk) to communicate with iRacing. The module can be installed via [pip](https://pip.pypa.io/en/stable/quickstart/), which will also install [PyYAML](https://pypi.python.org/pypi/PyYAML).

   ```bash
   $ pip install pyirsdk
   ```
3. [Download the repository](../../archive/master.zip) and unzip it. Place the resulting folder into your `Prismatik\Plugins` directory, located in your user folder. Rename the folder to remove the branch extension (e.g. '-master') so it only reads 'Prismatik-iRacing'. If the folder has the wrong name Prismatik won't properly load the configuration file.
4. Refresh the plugins list in Prismatik, and the iRacing plugin should show up as "iRacing Integration (source)". You can run the plugin via Prismatik or directly from the "Prismatik-iRacing.py" file in the `src` folder.

## Compile to Executable
After getting the Python code to work on its own, you might wish to compile your changes into a standalone executable. To compile the Python plugin to an executable I'm using the [PyInstaller](http://www.pyinstaller.org/) module.
1. Download PyInstaller using pip (see the information in step #2 above).
2. Open a console in the `Prismatik-iRacing\src` directory. This does **not** need to be done with elevated privileges.
3. Use the following command to build the executable:

   ```batch
   pyinstaller Prismatik-iRacing.py --onefile --icon ../icons/icon.ico --version-file version.py
   ```
   This will build the a standalone executable using the program's icon and the Windows-specific [versioning information](https://msdn.microsoft.com/en-us/library/ms646997.aspx).
4. If you want to launch the executable from Prismatik, you'll need to modify the 'Prismatik-iRacing.ini' file from the repository to point to your newly created executable, rather than to the Python script.
