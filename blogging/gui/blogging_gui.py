#################
##   imports   ##
#################

import sys
from datetime import datetime
from .imports import *  #imports were getting too messy, made a seperate file


####################
##  BLOGGING GUI  ##    now on main
####################


class BloggingGUI(QMainWindow):

    """main window for the blogging system's GUI"""


    #####################
    ##  LOGIN methods  ##     
    #####################  

    def handle_login_clicked(self):
        """process login attempt, update the ui, blog table on success"""
        h.handle_login_clicked(self)

    def handle_logout_clicked(self):
        """log out current user, reset login ui"""
        h.handle_logout_clicked(self)

    ####################
    ##  BLOG methods  ##     
    ####################    

    #these methods delegate to blogging_gui_handlers
    #handled in a seperate file to reduce clutter    

    def handle_new_blog_clicked(self):
        """opens the new blog dialogue, creates blog via controller, refreshs table"""
        h.handle_new_blog_clicked(self)


    def refresh_blogs(self):
        """re loads and displays all blogs in the blogs table"""
        h.refresh_blogs(self)


    def handle_blog_selection_changed(self, selected, deselected):
        """row selected in blogs table, sets current blog, shows posts"""
        h.handle_blog_selection_changed(self, selected, deselected)


    def handle_edit_blog_clicked(self):
        """edit currently selected blog"""
        h.handle_edit_blog_clicked(self)


    def handle_delete_blog_clicked(self):
        """delete currently selected blog"""
        h.handle_delete_blog_clicked(self)


    def handle_search_blog_clicked(self):
        """search blogs by name, update table"""
        h.handle_search_blog_clicked(self)


    def handle_clear_blog_search_clicked(self):
        """clear blog search, show all blogs"""
        h.handle_clear_blog_search_clicked(self)


    ####################
    ##  POST methods  ##     
    #################### 

    def refresh_posts(self):
        """re loads and displays posts for the current blog in the posts text area"""
        h.refresh_posts(self)


    def handle_new_post_clicked(self):
        """create new post in the current blog"""
        h.handle_new_post_clicked(self)


    def handle_edit_post_clicked(self):
        """edit existing post in current blog"""
        h.handle_edit_post_clicked(self)


    def handle_delete_post_clicked(self):
        """delete post from current blog"""
        h.handle_delete_post_clicked(self)


    def handle_list_posts_clicked(self):
        """refresh, lists all posts for current blog"""
        h.refresh_posts(self)


    ##############
    ##   init   ##
    ##############

    def __init__(self):

        super().__init__()
        self.selected_blog_id = None


        ################
        ##   setup    ##
        ################

        #config and controller, set autosave, controller
        self.configuration = Configuration()            #get config
        self.configuration.__class__.autosave = True    #persistence
        self.controller = Controller()                  #get controller

        #main window properties
        self.setWindowTitle("Blogging GUI")     #title
        self.resize(1280, 720)                  #window size

        #root widget, layout
        central = QWidget(self)
        main_layout = QVBoxLayout(central)
        central.setLayout(main_layout)
        self.setCentralWidget(central)


        ################
        ##   login    ##
        ################

        #top login row
        login_row = QHBoxLayout()

        #username
        self.username_edit = QLineEdit()                    #username
        self.username_edit.setPlaceholderText("Username")   #placeholder

        #password
        self.password_edit = QLineEdit()                    #password
        self.password_edit.setPlaceholderText("Password")   #placeholder
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password) #masked

        #buttons for login and logout
        self.login_button = QPushButton("Log in")
        self.logout_button = QPushButton("Log out")
        self.logout_button.setEnabled(False) #enables after login

        #login status label
        self.login_status_label = QLabel("Not Logged In")
        self.login_status_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | 
            Qt.AlignmentFlag.AlignVCenter
        )


        #assemble login row
        login_row.addWidget(QLabel("User: "))
        login_row.addWidget(self.username_edit)
        login_row.addWidget(self.password_edit)
        login_row.addWidget(self.login_button)
        login_row.addWidget(self.logout_button)
        login_row.addWidget(self.login_status_label, stretch=1)

        #add login row to main layout
        main_layout.addLayout(login_row)

        
        ################
        ##   BLOGS    ##
        ################

        #main tab, no other tabs used, this was redundant but I forgot to remove until last minute
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, stretch=1)

        #main tab, blogs on left, posts on right
        main_tab = QWidget()
        main_tab_layout = QHBoxLayout(main_tab)

        #BLOGS COLUMN
        blogs_column = QVBoxLayout()

        #header row for title and actions
        blogs_header_row = QHBoxLayout()
        blogs_label = QLabel("Blogs")

        #buttons
        self.button_new_blog = QPushButton("New Blog")
        self.button_edit_blog = QPushButton("Edit Blog")
        self.button_delete_blog = QPushButton("Delete Blog")

        blogs_header_row.addWidget(blogs_label)
        blogs_header_row.addStretch(1)
        blogs_header_row.addWidget(self.button_new_blog)
        blogs_header_row.addWidget(self.button_edit_blog)
        blogs_header_row.addWidget(self.button_delete_blog)

        blogs_column.addLayout(blogs_header_row)

        #search row for blogs, text field, seach/clear
        search_row = QHBoxLayout()
        self.blog_search_edit = QLineEdit()
        self.blog_search_edit.setPlaceholderText("Search blogs by name...")

        self.button_search_blog = QPushButton("Search")
        self.button_clear_blog_search = QPushButton("Clear")

        search_row.addWidget(self.blog_search_edit)
        search_row.addWidget(self.button_search_blog)
        search_row.addWidget(self.button_clear_blog_search)

        blogs_column.addLayout(search_row)

        #blog table
        self.blogs_table = QTableView()
        self.blogs_table.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Policy.Expanding, 
                QSizePolicy.Policy.Expanding
                )
        )

        blogs_column.addWidget(self.blogs_table)

        #start empty, then populate after login
        self.blogs_model = BlogsTableModel([])
        self.blogs_table.setModel(self.blogs_model)

        #configure selections
        self.blogs_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.blogs_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.blogs_table.horizontalHeader().setStretchLastSection(True)

        #selection change
        self.blogs_table.selectionModel().selectionChanged.connect(
            self.handle_blog_selection_changed
        )


        ###############
        ##   POSTS   ##
        ###############

        #POST COLUMN, rhs
        posts_column = QVBoxLayout()

        #header row
        posts_header_row = QHBoxLayout()
        posts_label = QLabel("Posts (current blog)")

        #buttons for managing post
        self.button_new_post    = QPushButton("New Post")
        self.button_edit_post   = QPushButton("Edit Post")
        self.button_delete_post = QPushButton("Delete Post")
        self.button_list_posts  = QPushButton("Refresh Posts")

        posts_header_row.addWidget(posts_label)
        posts_header_row.addStretch(1)
        posts_header_row.addWidget(self.button_new_post)
        posts_header_row.addWidget(self.button_edit_post)
        posts_header_row.addWidget(self.button_delete_post)
        posts_header_row.addWidget(self.button_list_posts)

        posts_column.addLayout(posts_header_row)

        #posts text area
        self.posts_text = QPlainTextEdit()
        self.posts_text.setReadOnly(True)
        posts_column.addWidget(self.posts_text)

        #add blogs and posts to main tab
        main_tab_layout.addLayout(blogs_column, stretch=2)
        main_tab_layout.addLayout(posts_column, stretch=3)

        #add main tab
        self.tabs.addTab(main_tab, "Main")
        
        #bottom status bar
        status = QStatusBar()

        self.setStatusBar(status)
        self.statusBar().showMessage("Ready")

        #####################
        ##  signals slots  ##
        #####################

        #login/logout actions
        self.login_button.clicked.connect(self.handle_login_clicked)
        self.logout_button.clicked.connect(self.handle_logout_clicked)
        
        #blog actions
        self.button_new_blog.clicked.connect(self.handle_new_blog_clicked)
        self.button_edit_blog.clicked.connect(self.handle_edit_blog_clicked)
        self.button_delete_blog.clicked.connect(self.handle_delete_blog_clicked)
        self.button_search_blog.clicked.connect(self.handle_search_blog_clicked)
        self.button_clear_blog_search.clicked.connect(self.handle_clear_blog_search_clicked)
        

        #post actions
        self.button_new_post.clicked.connect(self.handle_new_post_clicked)
        self.button_edit_post.clicked.connect(self.handle_edit_post_clicked)
        self.button_delete_post.clicked.connect(self.handle_delete_post_clicked)
        self.button_list_posts.clicked.connect(self.handle_list_posts_clicked)


def main():
    
    app = QApplication(sys.argv)

    ####EXTERNAL STYLE SHEET
    apply_global_style(app)


    window = BloggingGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
