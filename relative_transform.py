from PySide6 import QtCore as qc
from PySide6 import QtWidgets as qg
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import maya.cmds as cmds
import shiboken6


def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    return shiboken6.wrapInstance(int(ptr), qg.QWidget) if ptr else None


def gizmo_axes():
    """World-space X, Y and Z axes of the Move tool's current orientation."""
    ctx = "Move"
    mode = cmds.manipMoveContext(ctx, query=True, mode=True)
    if mode == 2:  # World
        return om.MVector(1, 0, 0), om.MVector(0, 1, 0), om.MVector(0, 0, 1)
    # Object, Component, Parent, Custom ...: Maya reports the gizmo rotation (radians)
    rx, ry, rz = cmds.manipMoveContext(ctx, query=True, orientAxes=True)
    m = om.MEulerRotation(rx, ry, rz).asMatrix()
    return (om.MVector(1, 0, 0) * m,
            om.MVector(0, 1, 0) * m,
            om.MVector(0, 0, 1) * m)


class SetPosition(qg.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, qc.Qt.FramelessWindowHint)
        self.setAttribute(qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Set Position")
        self.setFixedSize(150, 40)

        layout = qg.QHBoxLayout(self)
        self.entries = []
        for colour in ("255,0,0", "0,255,0", "0,0,255"):
            e = qg.QLineEdit()
            e.setStyleSheet(
                f"QLineEdit {{ border: 1px solid rgba({colour},0.5); border-radius: 2px; }}")
            e.returnPressed.connect(self.apply)
            layout.addWidget(e)
            self.entries.append(e)

        self._watching = False
        # start the click-away check only after the dialog has focus
        qc.QTimer.singleShot(200, self._start_watching)

    def _start_watching(self):
        qg.QApplication.instance().focusChanged.connect(self._focus_changed)
        self._watching = True

    def _value(self, entry):
        try:
            return float(entry.text().replace(",", ".") or 0)
        except ValueError:
            return 0.0

    def apply(self):
        x, y, z = (self._value(e) for e in self.entries)
        sel = cmds.ls(selection=True)
        print("SetPosition input:", x, y, z, "selection:", sel)
        if sel:
            ax, ay, az = gizmo_axes()
            d = ax * x + ay * y + az * z  # offset along the gizmo axes
            print("SetPosition world offset:", d.x, d.y, d.z)
            cmds.move(d.x, d.y, d.z, relative=True, worldSpace=True)
        self.close()

    def keyPressEvent(self, event):
        if event.key() == qc.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def _focus_changed(self, old, new):
        if new is None or not self.isAncestorOf(new):
            self.close()

    def closeEvent(self, event):
        if self._watching:
            qg.QApplication.instance().focusChanged.disconnect(self._focus_changed)
            self._watching = False
        super().closeEvent(event)


def open_dialog():
    cmds.setToolTo("moveSuperContext")
    win = get_maya_window()
    dialog = SetPosition(win)
    dialog.show()
    if win:
        dialog.move(win.frameGeometry().center() - dialog.rect().center())
    dialog.activateWindow()
    dialog.entries[0].setFocus()


open_dialog()
