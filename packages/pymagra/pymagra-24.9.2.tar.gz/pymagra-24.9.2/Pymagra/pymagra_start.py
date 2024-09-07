"""
Last modification Aug 12 2024

@author: Hermann Zeyen <hermann.zeyen@universite-paris-saclay.fr>
         Universite Paris-Saclay, France

Wrapper for PyMaGra program
"""

import sys
from pathlib import Path
from PyQt5 import QtWidgets

#import Pymagra as pmg
from Pymagra import PyMaGra

if __name__ == "__main__":
    # dir0 = r"D:/Tadjikistan/ZolIZard/"
    # dir0 = r"D:/Documents/Cours/Stages/M1/2023-24/Magnetics/2023-09-24"
    dir0 = r"E:/Daten/Fontaines_Salées_BRGM"
    # dir0 = "."

    def my_exception_hook(exctype, value, tracebk):
        """
        Not clear what it is good for.
        The problem is that usually no error messages are passed from
        QT.
        I found this in the internet, but it seems it does not work either...

        Parameters
        ----------
        exctype : TYPE
            DESCRIPTION.
        value : TYPE
            DESCRIPTION.
        tracebk : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        print(exctype, value, tracebk)
        sys._excepthook(exctype, value, tracebk)
        sys.exit(1)

    if __name__ == "__main__" and __package__ is None:
        file = Path(__file__).resolve()
        parent, top = file.parent, file.parents[0]

        sys.path.append(str(top))
        try:
            sys.path.remove(str(parent))
        except ValueError:  # Already removed
            pass
        if top not in sys.path:
            sys.path.append(top)

        __package__ = "Pymagra"

    try:
        app = QtWidgets.QApplication(sys.argv)
        sys._excepthook = sys.excepthook
        sys.excepthook = my_exception_hook
        # main = pmg.PyMaGra.Main(dir0)
        main = PyMaGra.Main(dir0)
        main.w.showMaximized()
        sys.exit(app.exec_())
    except Exception as error:
        print(f'An unexpected exception occurred: {error}.')
        #        sys.exit()
        pass
