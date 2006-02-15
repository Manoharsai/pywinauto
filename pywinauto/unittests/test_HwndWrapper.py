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

"Tests for HwndWrapper"

from pywinauto.application import Application
from pywinauto.controls.HwndWrapper import HwndWrapper
from pywinauto import win32structures, win32defines
import time
import pprint
import pdb

__revision__ = "$Revision: 234 $"

try:
    from pywinauto.controls.HwndWrapper import *
except ImportError:
    # allow it to be imported in a dev environment
    import sys

    pywinauto_imp = "\\".join(__file__.split('\\')[:-3])
    print "sdfdsf", pywinauto_imp
    sys.path.append(pywinauto_imp)
    from pywinauto.controls.HwndWrapper import *

import unittest

class HwndWrapperTests(unittest.TestCase):
    "Unit tests for the TreeViewWrapper class"

    def setUp(self):
        """Start the application set some data and ensure the application
        is in the state we want it."""

        # start the application
        self.app = Application()
        self.app.start_("calc.exe")

        self.dlg = self.app.Calculator
        self.ctrl = HwndWrapper(self.dlg.Backspace.handle)

    def tearDown(self):
        "Close the application after tests"
        # close the application
        self.dlg.TypeKeys("%{F4}")

    #def testText(self):
    #    "Test getting the window Text of the dialog"
    #    self.assertEquals(self.dlg.WindowText(), "Untitled - Notepad")

    def testFriendlyClassName(self):
        "Test getting the friendly classname of the dialog"
        self.assertEquals(self.ctrl.FriendlyClassName(), "Button")

    def testClass(self):
        "Test getting the classname of the dialog"
        self.assertEquals(self.ctrl.Class(), "Button")

    def testWindowText(self):
        "Test getting the window Text of the dialog"
        self.assertEquals(self.ctrl.WindowText(), "Backspace")

    def testStyle(self):

        self.dlg.Style()

        self.assertEquals(self.ctrl.Style(),
            win32defines.WS_CHILD |
            win32defines.WS_VISIBLE |
            win32defines.BS_PUSHBUTTON |
            win32defines.BS_TEXT)


    def testExStyle(self):
        self.assertEquals(self.ctrl.ExStyle(),
            win32defines.WS_EX_NOPARENTNOTIFY |
            win32defines.WS_EX_LEFT |
            win32defines.WS_EX_LTRREADING |
            win32defines.WS_EX_RIGHTSCROLLBAR)

        self.assertEquals(self.dlg.ExStyle(),
            win32defines.WS_EX_WINDOWEDGE |
            win32defines.WS_EX_LEFT |
            win32defines.WS_EX_LTRREADING |
            win32defines.WS_EX_RIGHTSCROLLBAR |
            win32defines.WS_EX_CONTROLPARENT |
            win32defines.WS_EX_APPWINDOW)

    def testControlID(self):
        self.assertEquals(self.ctrl.ControlID(), 83)
        self.dlg.ControlID()

    def testUserData(self):
        self.ctrl.UserData()
        self.dlg.UserData()

    def testContextHelpID(self):
        self.ctrl.ContextHelpID()
        self.dlg.ContextHelpID()

    def testIsVisible(self):
        self.assertEqual(self.ctrl.IsVisible(), True)
        self.assertEqual(self.dlg.IsVisible(), True)

    def testIsUnicode(self):
        self.assertEqual(self.ctrl.IsUnicode(), True)
        self.assertEqual(self.dlg.IsUnicode(), True)

    def testIsEnabled(self):
        self.assertEqual(self.ctrl.IsEnabled(), True)
        self.assertEqual(self.dlg.IsEnabled(), True)
        self.assertEqual(self.dlg.window_(title = 'Ave', enabled_only = False).IsEnabled(), False)

    def testRectangle(self):
        "Test getting the rectangle of the dialog"
        rect = self.dlg.Rectangle()
        self.assertNotEqual(rect.top, None)
        self.assertNotEqual(rect.left, None)
        self.assertNotEqual(rect.bottom, None)
        self.assertNotEqual(rect.right, None)

        self.assertEqual(rect.height(), 309)
        self.assertEqual(rect.width(), 480)

    def testClientRect(self):
        rect = self.dlg.Rectangle()
        cli = self.dlg.ClientRect()

        self.assertEqual(cli.left , 0)
        self.assertEqual(cli.top , 0)

        assert(cli.width() < rect.width())
        assert(cli.height() < rect.height())

    def testFont(self):
        self.assertNotEqual(self.dlg.Font(), self.ctrl.Font())

    def ProcessID(self):
        self.assertEqual(self.ctrl.ProcessID(), self.dlg.ProcessID)
        self.assertNotEqual(self.ctrl.ProcessID(), 0)

    def testHasStyle(self):
        self.assertEqual(self.ctrl.HasStyle(win32defines.WS_CHILD), True)
        self.assertEqual(self.dlg.HasStyle(win32defines.WS_CHILD), False)

        self.assertEqual(self.ctrl.HasStyle(win32defines.WS_SYSMENU), False)
        self.assertEqual(self.dlg.HasStyle(win32defines.WS_SYSMENU), True)


    def testHasExStyle(self):
        self.assertEqual(self.ctrl.HasExStyle(win32defines.WS_EX_NOPARENTNOTIFY), True)
        self.assertEqual(self.dlg.HasExStyle(win32defines.WS_EX_NOPARENTNOTIFY), False)

        self.assertEqual(self.ctrl.HasExStyle(win32defines.WS_EX_APPWINDOW), False)
        self.assertEqual(self.dlg.HasExStyle(win32defines.WS_EX_APPWINDOW), True)

    def testIsDialog(self):
        self.assertEqual(self.ctrl.IsDialog(), False)
        self.assertEqual(self.dlg.IsDialog(), True)

    def testMenuItems(self):
        self.assertEqual(self.ctrl.MenuItems(), [])

        self.assertEqual(self.dlg.MenuItems()[1]['Text'], '&View')

    def testParent(self):
        self.assertEqual(self.ctrl.Parent(), self.dlg.handle)

    def testTopLevelParent(self):
        self.assertEqual(self.ctrl.TopLevelParent(), self.dlg.handle)
        self.assertEqual(self.dlg.TopLevelParent(), self.dlg.handle)

    def testTexts(self):
        self.assertEqual(self.dlg.Texts(), [u'Calculator'])
        self.assertEqual(self.ctrl.Texts(), [u'Backspace'])

        self.assertEqual(self.dlg.Edit.Texts(), ['', "0. "])

    def testClientRects(self):
        self.assertEqual(self.ctrl.ClientRects()[0], self.ctrl.ClientRect())
        self.assertEqual(self.dlg.ClientRects()[0], self.dlg.ClientRect())

    def testFonts(self):
        self.assertEqual(self.ctrl.Fonts()[0], self.ctrl.Font())
        self.assertEqual(self.dlg.Fonts()[0], self.dlg.Font())

    def testChildren(self):
        self.assertEqual(self.ctrl.Children(), [])
        self.assertNotEqual(self.dlg.Children(), [])


    def testIsChild(self):
        self.assertEqual(self.ctrl.IsChild(self.dlg.ctrl_()), True)
        self.assertEqual(self.dlg.IsChild(self.ctrl), False)


#    def testSendMessage(self):
#        pass
#    def testSendMessageTimeout(self):
#        pass
#    def testPostMessage(self):
#        pass
#    def testNotifyMenuSelect(self):
#        pass
#    def testNotifyParent(self):
#        pass

    def testGetProperties(self):
        "Test getting the properties for the control"
        props  = self.dlg.GetProperties()

        self.assertEquals(
            self.dlg.FriendlyClassName(), props['FriendlyClassName'])

        self.assertEquals(
            self.dlg.Texts(), props['Texts'])

        for prop_name in props:
            self.assertEquals(getattr(self.dlg, prop_name)(), props[prop_name])

#    def testCaptureAsImage(self):
#        pass

    def testEquals(self):
        self.assertNotEqual(self.ctrl, self.dlg.handle)
        self.assertEqual(self.ctrl, self.ctrl.handle)
        self.assertEqual(self.ctrl, self.ctrl)


#    def testVerifyActionable(self):
#        self.assertRaises()

#    def testVerifyEnabled(self):
#        self.assertRaises()

#    def testVerifyVisible(self):
#        self.assertRaises()


#    def testClick(self):
#        pass
#
#    def testCloseClick(self):
#        pass
#
#    def testDoubleClick(self):
#        pass
#
#    def testRightClick(self):
#        pass
#
#    def testPressMouse(self):
#        pass
#
#    def testReleaseMouse(self):
#        pass
#
#    def testMoveMouse(self):
#        pass
#
#    def testDragMouse(self):
#        pass
#
#    def testSetWindowText(self):
#        pass
#
#    def testTypeKeys(self):
#        pass
#
#    def testDebugMessage(self):
#        pass
#
#    def testDrawOutline(self):
#        pass
#
#    def testMenuSelect(self):
#        pass
#

    def testMoveWindow_same(self):
        "Test calling movewindow without any parameters"
        prevRect = self.dlg.Rectangle()
        self.dlg.MoveWindow()
        self.assertEquals(prevRect, self.dlg.Rectangle())

    def testMoveWindow(self):
        "Test moving the window"

        dlgClientRect = self.dlg.ClientAreaRect()

        prev_rect = self.ctrl.Rectangle() - dlgClientRect

        new_rect = win32structures.RECT(prev_rect)
        new_rect.left -= 1
        new_rect.top -= 1
        new_rect.right += 2
        new_rect.bottom += 2

        self.ctrl.MoveWindow(
            new_rect.left,
            new_rect.top,
            new_rect.width(),
            new_rect.height(),
            )

        self.assertEquals(
            self.ctrl.Rectangle(),
            new_rect + dlgClientRect)

        self.ctrl.MoveWindow(prev_rect)

        self.assertEquals(
            self.ctrl.Rectangle(),
            prev_rect + dlgClientRect)

    def testGetFocus(self):
        self.assertNotEqual(self.dlg.GetFocus(), None)
        self.assertEqual(self.dlg.GetFocus(), self.ctrl.GetFocus())

        self.dlg.Hyp.SetFocus()
        self.assertEqual(self.dlg.GetFocus(), self.dlg.Hyp.handle)


    def testSetFocus(self):
        self.assertNotEqual(self.dlg.GetFocus(), self.dlg.Hyp.handle)
        self.dlg.Hyp.SetFocus()
        self.assertEqual(self.dlg.GetFocus(), self.dlg.Hyp.handle)




##====================================================================
#def _unittests():
#    "do some basic testing"
#    from pywinauto.findwindows import find_windows
#    import sys
#
#    if len(sys.argv) < 2:
#        handle = win32functions.GetDesktopWindow()
#    else:
#        try:
#            handle = int(eval(sys.argv[1]))
#
#        except ValueError:
#
#            handle = find_windows(
#                title_re = "^" + sys.argv[1],
#                class_name = "#32770",
#                visible_only = False)
#
#            if not handle:
#                print "dialog not found"
#                sys.exit()
#
#    props = GetDialogPropsFromHandle(handle)
#    print len(props)
#    #pprint(GetDialogPropsFromHandle(handle))


if __name__ == "__main__":
    unittest.main()
