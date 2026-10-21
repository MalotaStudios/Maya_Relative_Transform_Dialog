Select any objects or components and run the script. A small dialog opens where you type a distance for each axis. Press Enter and the selection moves by that amount along the current Move tool gizmo orientation (World, Object, Component or Custom), not just world X, Y, Z. Distances use your current scene unit, and both 1.5 and 1,5 work as decimals. Each move is a single undo step, and the dialog closes by itself when you click back into Maya.

For older Maya versions you have to edit import of PySide and shiboken.
Example:

Maya 2025:
```
from PySide6 import QtCore as qc
from PySide6 import QtWidgets as qg
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import shiboken6 as shiboken
```

Maya 2022:
```
from PySide2 import QtCore as qc
from PySide2 import QtWidgets as qg
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import shiboken2 as shiboken
```



