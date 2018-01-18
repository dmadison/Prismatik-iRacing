# iRacing Plugin for Prismatik - Build Instructions
If you'd like to work with the plugin's source, here are some instructions to help you along the way.

## Source Setup
The repository can be used as-is to run the plugin from source, assuming you have Python and the required dependencies installed.

### Python and Dependencies
1. Install [Python 3](https://www.python.org/downloads/). This plugin was written with Python 3.6, and earlier versions may not be compatible.
     * If you're using Windows, you'll need to [add Python to your system's 'PATH' environmental variable.](https://docs.python.org/using/windows.html#excursus-setting-environment-variables) Be sure to include the scripts directory as well in order to use modules from the command line.
2. This plugin relies on the [pyirsdk library](https://github.com/kutu/pyirsdk) to communicate with iRacing. The module can be installed via [pip](https://pip.pypa.io/en/stable/quickstart/), which will also install [PyYAML](https://pypi.python.org/pypi/PyYAML).

   ```bash
   $ pip install pyirsdk
   ```
3. [Download the repository](../../archive/master.zip) and unzip it. Place the resulting folder into your `Prismatik\Plugins` directory, located in your user folder. Rename the folder to remove the branch extension (e.g. '-master') so that it reads 'Prismatik-iRacing-source'. If the folder and configuration file's names do not match Prismatik won't be able to load the plugin.
4. Refresh the plugins list in Prismatik, and the iRacing plugin should show up as "iRacing Integration (source)". You can run the plugin via Prismatik or directly from the "Prismatik-iRacing.py" file in the `src` folder.

If you want to have multiple copies of the source available as plugins, you will need to change the name of the `Prismatik-iRacing-source.ini` configuration file to match the name of its parent folder within `Plugins`. You will also need to change the file's "Name" property so that it does not conflict with any other versions you have installed.

## Bundle to Executable
After getting the Python code to work on its own, you might wish to bundle your changes into a standalone executable. To do this I'm using the [PyInstaller](http://www.pyinstaller.org/) module.
1. Download PyInstaller using pip.
2. Open a console in the `Prismatik-iRacing\src` directory. This does **not** need to be done with elevated privileges.
3. Use the following command to build the executable:

   ```batch
   pyinstaller Prismatik-iRacing.py --onedir --noconsole --icon ../icons/icon.ico --version-file build/version_info.py
   ```
   This will build the a standalone executable using the program's icon and the Windows-specific [versioning information](https://msdn.microsoft.com/en-us/library/ms646997.aspx). You can change `--onedir` to `--onefile` if you'd like to build a single executable, but be aware that this won't work properly if activated via Prismatik (see [#11](https://github.com/dmadison/Prismatik-iRacing/issues/11)). You can remove the `--noconsole` option if you would like to see the debug information. You can find more information on build flags in [the PyInstaller manual](https://pythonhosted.org/PyInstaller/usage.html).
4. If you want to launch the executable via the Prismatik plugins manager, you'll need to modify the 'Prismatik-iRacing-source.ini' file from the repository to point to your newly created executable, rather than to the Python program.

## Scripts
There are two scripts in the repository to aid with building and distributing the plugin. Although I mostly put them together for fun and practice.

### Release Assembler
The release assembler ([`release_assembler.py`](release_assembler.py)) is the larger of the two scripts. After building the `--onedir` executable using the instructions above, this script will gather the executable, icon, and configuration files into a single zip archive ready for deployment.

The script also modifies the plugin configuration file to point to the icon and executable in the standalone executable's modified folder structure. This lets me keep the repository as-is for source development while quicking rendering the proper configuration file for the standalone executable. It also enables me to keep both the source and standalone versions active as available plugins in Prismatik, which is useful for debugging.

### Version Updater
The smaller of the two scripts, the version updater([`version_updater.py`](version_updater.py)) takes user input for the latest [semantic versioning](https://semver.org/) numbers and updates the corresponding files in the repository. Namely the plugin configuration file ([`Prismatik-iRacing-source.ini`](../../Prismatik-iRacing-source.ini)) and the version info file ([`version_info.py`](version_info.py)):
```bash
Prismatik-iRacing Plugin: Version Update Script
----------
Major #? 0
Minor #? 2
Patch #? 3
You inputted 0.2.3. Is that correct? (y/n) y
Version number looks good, let's do some stuff!
```
It's a little rough around the edges, but it seems to do the job alright!
