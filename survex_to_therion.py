#!/usr/bin/python

##
## Copyright (C) 2011-2019 Andrew Atkinson
##
##-------------------------------------------------------------------
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##-------------------------------------------------------------------

import argparse
import os
import re

from datetime import datetime
from os.path import join

def OverWriteFile():
    print("click!")

def RenameFile():
    print("click2!")
    print(FullPathName)
    file_path = tkFileDialog.asksaveasfilename(title="New file", defaultextension=".th", filetypes=[("th file", ".th"), ("All files", ".*")])
    print(file_path)

def ExistingFile(Name):
    master = Tk()
    master.title("Existing File")
    Label(text="File already exists!\n\n" + Name + "\n\nWhat do you want to do with the file?").pack(padx=50, pady=10)
    SameName = Button(master, text="Over Write!", command=OverWriteFile)
    SameName.pack(side=LEFT, padx=50, pady=10)
    ReName = Button(master, text="Rename", command=RenameFile)
    ReName.pack(side=RIGHT, padx=50, pady=10)
    mainloop()
    return Name

def Convert(SvxList):
    if re.search(r'\;', SvxList) is not None:
        SvxList = re.sub(r'\;', '#', SvxList)
    if re.search(r'^\s*\*', SvxList) is not None:
        CavernCommand = re.search(r'^(\s*)\*(\w+)(.*)', SvxList)
        ComList = ['team', 'instruments', 'copyright']
        CavCom = CavernCommand.group(2).lower()
        if CavCom == "begin":
            ThList = CavernCommand.group(1) + "survey" + CavernCommand.group(3) + "\ncentreline\n"
        elif CavCom == "end":
            ThList = CavernCommand.group(1) + "endcentreline\nendsurvey\n"
        elif CavCom == "include":
            TempList = CavernCommand.group(1) + "input" + CavernCommand.group(3) + "\n"
            TempList = re.sub(r'\.svx', '.th', TempList)
            #change \ to /
            ThList = re.sub(r'\\', r'/', TempList)
        elif CavCom == "equate":
            EquateStn = str.split(CavernCommand.group(3))
            ThList = CavernCommand.group(1) + CavernCommand.group(2).lower()
            for stn in EquateStn:
                print(stn)
                if re.search(r'(\..+$)', stn) is not None:
                    thstn = re.search(r'(.+)\.(.+?$)', stn)
                    # Split by dots, reverse, and rejoin
                    location_parts = thstn.group(1).split('.')
                    location_parts.reverse()
                    reversed_location = '.'.join(location_parts)
                    Station = thstn.group(2) + "@" + reversed_location
                else:
                    Station = stn
                ThList = ThList + " " + Station
            ThList += "\n"
            print(ThList)
        elif ((CavCom == "require") or (CavCom == "export") or (CavCom == "ref")):
            ThList = CavernCommand.group(1) + "# " + CavernCommand.group(2).lower() + CavernCommand.group(3) + "\n"
        elif CavCom in ComList:
            ThList = CavernCommand.group(1) + CavernCommand.group(2).lower() + CavernCommand.group(3) + "\n"
        else:
            ThList = CavernCommand.group(1) + CavernCommand.group(2).lower() + CavernCommand.group(3).lower() + "\n"
    else:
        ThList = SvxList
    return ThList

def ToTherion(SvxName, ThName):
    with open(SvxName, "r") as File:
        FileList = File.readlines()
    TherionList = TherionHeaders(SvxName) + [Convert(Line) for Line in FileList]
    with open(ThName, "w") as ThFile:
        ThFile.writelines(TherionList)
    return TherionList

def TherionHeaders(SvxName):
    ThHeaders = []
    ThHeaders.append("encoding UTF-8\n")
    ThHeaders.append("\n")
    ThHeaders.append("#\n")
    ThHeaders.append("# automatically created from " + SvxName + "\n")
    try:
        script_path = __file__
        script_name = os.path.basename(script_path)
    except NameError:
        script_name = "survex_to_therion.py"
    ThHeaders.append("# by " + script_name + "\n")
    now = datetime.now()
    iso_format = now.isoformat()
    ThHeaders.append("# at " + iso_format + "\n")
    ThHeaders.append("#\n")
    ThHeaders.append("\n")
    return ThHeaders

def process_directory(directory):
    global i
    for FullName in os.listdir(directory):
        if svx.search(FullName) is not None:
            i += 1
            print("File number ===================================", i)
            print(FullName)
            FullPathName = join(directory, FullName)
            BaseName = svx.split(FullName)
            FullName = BaseName[0] + ".th"
            FullPathNameth = join(directory, FullName)
            ToTherion(FullPathName, FullPathNameth)

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--no-recurse', action='store_true', help='Process files only in the current directory')
args = parser.parse_args()

svx = re.compile(r'\.svx', re.IGNORECASE)
i = 1

if args.no_recurse:
    process_directory('.')
else:
    for root, dirs, files in os.walk('.'):
        if '.svn' in dirs:
            dirs.remove('.svn')
        process_directory(root)