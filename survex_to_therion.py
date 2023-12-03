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

import os, re
#from Tkinter import *
#import tkFileDialog

from os.path import join


def OverWriteFile():
    print ("click!")

def RenameFile():
    print ("click2!")
    print FullPathName
    file_path = tkFileDialog.asksaveasfilename(title="New file",defaultextension=".th", filetypes=[("th file",".th"),("All files",".*")])# filename = tk.filedialog.askopenfilename()
    print file_path

def ExistingFile(Name):
    master = Tk()
    master.title("Existing File")
    Label(text="File already exists!\n\n"+Name+"\n\nWhat do you want to do with the file?").pack(padx=50, pady=10)
    SameName = Button(master, text="Over Write!", command=OverWriteFile)
    SameName.pack(side=LEFT,padx=50, pady=10)
    ReName = Button(master, text="Rename", command=RenameFile)
    ReName.pack(side=RIGHT, padx=50, pady=10)
    mainloop()
    return Name

def Convert(SvxList):
    if re.search(r'\;',SvxList) != None:
         SvxList = re.sub(r'\;','#',SvxList)
    if re.search(r'^\s*\*',SvxList) != None:
        CavernCommand = re.search(r'^(\s*)\*(\w+)(.*)',SvxList)
        #A lst of commands that do not get the text lowercased, along with begin and end
        ComList = ['team', 'instuments', 'copyright']
        CavCom = CavernCommand.group(2).lower()
        if CavCom == "begin":
            ThList = CavernCommand.group(1) +"survey"+ CavernCommand.group(3) +"\ncentreline\n"
        elif CavCom == "end":
            ThList = CavernCommand.group(1) +"endcentreline\nendsurvey\n"
        elif CavCom == "include":
            TempList = CavernCommand.group(1) +"input"+CavernCommand.group(3)+"\n"
            TempList = re.sub(r'\.svx','.th',TempList)
            #change \ to /
            ThList = re.sub(r'\\',r'/',TempList )
        elif CavCom == "equate":
            EquateStn = str.split(CavernCommand.group(3))
            ThList = CavernCommand.group(1)+CavernCommand.group(2).lower()
            for stn in EquateStn:
                print stn
                if re.search(r'(\..+$)',stn) != None:
                    thstn = re.search(r'(.+)\.(.+?$)',stn)
                    Station = thstn.group(2)+"@"+thstn.group(1)
                else:
                    Station = stn
                ThList = ThList +" "+ Station
            ThList += "\n"
            print ThList
        elif ((CavCom == "require") or (CavCom == "export") or (CavCom == "ref")):
            ThList = CavernCommand.group(1) + "# " + CavernCommand.group(2).lower() + CavernCommand.group(3)+"\n"
        elif CavCom in ComList:
            ThList = CavernCommand.group(1)+CavernCommand.group(2).lower()+CavernCommand.group(3)+"\n"
        else:
            ThList = CavernCommand.group(1)+CavernCommand.group(2).lower()+CavernCommand.group(3).lower()+"\n"
    else:
        ThList = SvxList
    return ThList

def ToTherion(SvxName, ThName):
    File = open(SvxName,"U")
    FileList = File.readlines()
    TherionList = [Convert(Line) for Line in FileList]
    ThFile =open(ThName, "w")
    ThFile.writelines(TherionList)
    return TherionList


svx = re.compile(r'\.svx', re.IGNORECASE)
i=1
for root, dirs, files in os.walk('.'):
    if '.svn' in dirs:
        dirs.remove('.svn')  # don't visit svn directories
    for FullName in files:

        if svx.search(FullName) != None:
            i=i+1
            print "File number ===================================",  i
            print FullName
            FullPathName = join(root, FullName)
            BaseName = svx.split(FullName)
            FullName = BaseName[0] + ".th"
            FullPathNameth = join(root, FullName)
            #Check to see if .th file (or directory!) already exits
            #if os.path.exists(FullPathNameth) == 1:
            #    FullPathNameth = ExistingFile(FullPathNameth)
            ToTherion(FullPathName, FullPathNameth)





