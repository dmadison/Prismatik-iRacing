#
# Project     Prismatik - iRacing Plugin
# @author     David Madison
# @link       github.com/dmadison/Prismatik-iRacing
# @license    GPLv3 - Copyright (c) 2018 David Madison
#
# This file is part of the Prismatik - iRacing Plugin.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0, 2, 3, 0),
    prodvers=(0, 2, 3, 0),
    mask=0x3f,     # Mask for valid flags
    flags=0x0,     # Compiler flags. None valid.
    OS=0x040004,   # Designed for Windows NT, 32-bit OS
    fileType=0x1,  # File is an application
    subtype=0x0,   # File is not a driver
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0', # U.S. English / Unicode
        [StringStruct(u'CompanyName', u''),
        StringStruct(u'FileDescription', u'iRacing Plugin for Prismatik'),
        StringStruct(u'FileVersion', u'0.2.3.0'),
		StringStruct(u'InternalName', u'Prismatik-iRacing'),
        StringStruct(u'LegalCopyright', u'\xa9 David Madison 2018'),
        StringStruct(u'ProductName', u'iRacing Plugin for Prismatik'),
        StringStruct(u'ProductVersion', u'0.2.3.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])]) # U.S. English / Unicode
  ]
)
