from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication


#global font
GLOBAL_FONT = QFont("consoloas", 10)

#constants

button_padding = "10px 18px"
background_colour = "#1e1e1e"
background_colour_2 = "#252526"
off_white = "#F9F9F9"
widget_border_colour = "#3c3c3c"


GLOBAL_STYLESHEET = """


/*///////////////////////////////////////
//////  main bcg and default text  //////
///////////////////////////////////////*/


/* main bcg */

QMainWindow 
{{
    background-color: {background_colour};
}}



/* default bcg and text colour */

QWidget 
{{
    background-color: {background_colour};
    color: green;
}}


/*//////////////////////////////////
//////  TEXT INPUTS & TABLES  //////
//////////////////////////////////*/



/* input areas */

QLineEdit, QPlainTextEdit, QTableView
{{
    background-color: {background_colour_2};
    color: {off_white};
    border: 1px solid {widget_border_colour};
}}



/* grid lines and selection colour */
    
QTableView
{{
    gridline-color: {widget_border_colour};
    selection-background-color: #0e639c;
    selection-color: {off_white};
}}



/* table header */


QHeaderView::section
{{
    background-color: #333333;
    color: {off_white};
    padding: 4px;
    border: 0px;
    border-right: 1px solid {widget_border_colour};
}}





/*/////////////////////
//////  buttons  //////
/////////////////////*/


/* default button */

QPushButton
{{
    background-color: #0e639c;
    color: {off_white};
    border-radius: 4px;
    padding: 4px 10px;
    border: 1px solid #0e639c;
}}


/* button hovered */

QPushButton:hover 
{{
    background-color: #1177bb;
}}


/* disabled button */

QPushButton:disabled
{{
    background-color: {widget_border_colour};
    color: #888888;
    border-color: {widget_border_colour};
}}





/*//////////////////
//////  tabs  //////
//////////////////*/



/* around tab main area */

QTabWidget::pane
{{
    border: 1px solid {widget_border_colour};
}}


/* normal tab */

QTabBar::tab
{{
    background-color: {background_colour};
    color: #f0f0f0;
    padding: {button_padding};
    margin: 20px 0px 0px 0px;
}}



/* current selected */

QTabBar::tab:selected
{{
    background-color: #2d2d2d;
    border-style: solid;
    border-color: {widget_border_colour};
    border-width: 1px 1px 0px 1px;
}}


/*////////////////////////
//////  status bar  //////
////////////////////////*/


/* status bar */

QStatusBar 
{{
    color: {off_white};
    

}}

QStatusBar QLabel
{{
    padding: 10px;
}}




/*/////////////////////////////
//////  history side tab //////
/////////////////////////////*/


/* history list */

QListWidget
{{
    background-color: {background_colour_2};
    color: #f0f0f0;
    border: 1px solid {widget_border_colour};

}}
""".format(
    button_padding=button_padding,
    background_colour=background_colour,
    background_colour_2=background_colour_2,
    off_white=off_white,
    widget_border_colour=widget_border_colour,
    )


def apply_global_style(app: QApplication) -> None:
    
    app.setFont(GLOBAL_FONT)
    app.setStyleSheet(GLOBAL_STYLESHEET)