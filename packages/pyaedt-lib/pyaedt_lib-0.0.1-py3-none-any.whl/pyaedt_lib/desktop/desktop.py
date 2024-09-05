import pyaedt

from pyaedt import Desktop

import os
import shutil

class LibDesktop(Desktop):

    def __init__(self, version=None, non_graphical=False, student_version=False):

        self.version = None
        self.non_graphical = False
        self.pid = None

        self.dir = os.path.expanduser('~/Documents/Ansoft')
        self.project_name = "script"

        super().__init__(version=version, non_graphical=non_graphical, student_version=student_version)



    def close_desktop(self) :

        super().close_desktop()