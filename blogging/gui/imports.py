#################
##   imports   ##
#################

#it was getting too messy in the main file


#######################
## qt core, widgets  ##
#######################

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QPlainTextEdit,
    QStatusBar,
    QSizePolicy,
    QTabWidget,
    QListWidget,
    QMessageBox,
    QDialog,
    QInputDialog,
)

#################
##  blogging   ##
#################

from blogging.configuration import Configuration    #config
from blogging.controller import Controller          #controller

from blogging.exception.illegal_access_exception import IllegalAccessException          #bad access
from blogging.exception.illegal_operation_exception import IllegalOperationException    #bad op

####################
##  gui additions ##
####################

from blogging.gui.styles import apply_global_style          #css
from blogging.gui.blogs_table_model import BlogsTableModel  #blog table class
from blogging.gui.blog_dialogue import BlogEditDialog       #blog dialogue class
from blogging.gui import blogging_gui_handlers as h         #method delegator