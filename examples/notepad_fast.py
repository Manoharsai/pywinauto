# GUI Application automation and testing library
# Copyright (C) 2006 Mark Mc Mahon
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
#    Free Software Foundation, Inc.,
#    59 Temple Place,
#    Suite 330,
#    Boston, MA 02111-1307 USA

"Run some automations to test things"

__revision__ = "$Revision: 214 $"

import time

try:
    from pywinauto import application
except ImportError:
    import os.path
    pywinauto_path = os.path.abspath(__file__)
    pywinauto_path = os.path.split(os.path.split(pywinauto_path)[0])[0]
    import sys
    sys.path.append(pywinauto_path)
    from pywinauto import application
from pywinauto import tests
from pywinauto.findbestmatch import MatchError
from pywinauto import findwindows

application.set_timing(2, .01, 10, .001, .001, 0, 0, 0, 0, 0)


app = application.Application()

## for distribution we don't want to connect to anybodies application
## because we may mess up something they are working on!
#try:
#    app.connect_(path = ur"c:\windows\system32\notepad.exe")
#except application.ProcessNotFoundError:
#    app.start_(ur"c:\windows\system32\notepad.exe")
app.start_(ur"notepad.exe")

app.Notepad.MenuSelect("File->PageSetup")

# ----- Page Setup Dialog ----
# Select the 4th combobox item
app.PageSetupDlg.ComboBox1.Select(4)

# Select the 'Letter' combobox item
app.PageSetupDlg.ComboBox1.Select("Letter")

# run some tests on the Dialog. List of available tests:
#        "AllControls",
#        "AsianHotkey",
#        "ComboBoxDroppedHeight",
#        "CompareToRefFont",
#        "LeadTrailSpaces",
#        "MiscValues",
#        "Missalignment",
#        "MissingExtraString",
#        "Overlapping",
#        "RepeatedHotkey",
#        "Translation",
#        "Truncation",

bugs = app.PageSetupDlg.RunTests('RepeatedHotkey Truncation')

# if there are any bugs they will be printed to the console
# and the controls will be highlighted
tests.print_bugs(bugs)

# ----- Next Page Setup Dialog ----
app.PageSetupDlg.Printer.Click()

# do some radio button clicks
# Open the Connect to printer dialog so we can
# try out checking/unchecking a checkbox
app.PageSetupDlg.Network.Click()

# ----- Connect To Printer Dialog ----
# Select a checkbox
app.ConnectToPrinter.ExpandByDefault.Check()

app.ConnectToPrinter.ExpandByDefault.UnCheck()

# try doing the same by using click
app.ConnectToPrinter.ExpandByDefault.Click()

app.ConnectToPrinter.ExpandByDefault.Click()

# close the dialog
app.ConnectToPrinter.Cancel.CloseClick()

# ----- 2nd Page Setup Dialog again ----
app.PageSetupDlg2.Properties.Click()

doc_props = app.window_(title_re = ".*Document Properties")

# ----- Document Properties Dialog ----
# some tab control selections
# Two ways of selecting tabs with indices...
doc_props.TabCtrl.Select(0)
doc_props.TabCtrl.Select(1)
doc_props.TabCtrl.Select(2)

# or with text...
doc_props.TabCtrl.Select("PaperQuality")
doc_props.TabCtrl.Select("JobRetention")
doc_props.TabCtrl.Select("Layout")


# do some radio button clicks
doc_props.RotatedLandscape.Click()
doc_props.BackToFront.Click()
doc_props.FlipOnShortEdge.Click()

doc_props.Portrait.Click()
doc_props._None.Click()
doc_props.FrontToBack.Click()

# open the Advanced options dialog in two steps
advbutton = doc_props.Advanced
advbutton.Click()

# close the 4 windows

# ----- Advanced Options Dialog ----
app.window_(title_re = ".* Advanced Options").Ok.Click()
# ----- Document Properties Dialog again ----
doc_props.Cancel.CloseClick()
# ----- 2nd Page Setup Dialog again ----
app.PageSetupDlg2.OK.CloseClick()
# ----- Page Setup Dialog ----
app.PageSetupDlg.Ok.CloseClick()

# type some text - note that extended characters ARE allowed
app.Notepad.Edit.SetEditText(u"I am typing s\xe4me text to Notepad\r\n\r\n"
    "And then I am going to quit")

app.Notepad.Edit.RightClick()
time.sleep(3)
app.Notepad.Edit.TypeKeys("{ESC}")

# the following shows that Sendtext does not accept
# accented characters - but does allow 'control' characters
app.Notepad.Edit.TypeKeys(u"{END}{ENTER}SendText d\xf6\xe9s not "
    u"s\xfcpp\xf4rt \xe0cce\xf1ted characters", with_spaces = True)

# Try and save
app.Notepad.MenuSelect("File->SaveAs")
app.SaveAs.ComboBox5.Select("UTF-8")
app.SaveAs.edit1.SetEditText("Example-utf8.txt")
app.SaveAs.Save.CloseClick()

# my machine has a weird problem - when connected to the network
# the SaveAs Dialog appears - but doing anything with it can
# cause a LONG delay - the easiest thing is to just wait
# until the dialog is no longer active

# - Dialog might just be gone - because click worked
# - dialog might be waiting to disappear
#   so can't wait for next dialog or for it to be disabled
# - dialog might be waiting to display message box so can't wait
#   for it to be gone or for the main dialog to be enabled.

# while the dialog exists wait upto 30 seconds (and yes it can
# take that long on my computer sometimes :-( )
app.SaveAs.Cancel.WaitNotEnabled()

try:
    app.SaveAs.Yes.CloseClick()
except MatchError:
    pass

# exit notepad
app.Notepad.MenuSelect("File->Exit")

if app.Notepad.No.Exists(1):
    app.Notepad.No.Click()