from PyQt6.QtWidgets import QMessageBox, QDialog, QInputDialog
from blogging.gui.blog_dialogue import BlogEditDialog



def get_selected_blog(gui):
    """
        #return blog obj for currently selected row, or none

    """
    #get selection model from table
    selection_model = gui.blogs_table.selectionModel()
    if selection_model is None: return None

    #get selected rows
    rows = selection_model.selectedRows()
    if not rows: return None
    row = rows[0].row()

    return gui.blogs_model.get_blog(row)



def handle_edit_blog_clicked(gui):
    """
        #edit currently selected blog

    """

    # require login
    try:
        _ = gui.controller.list_blogs()
    except Exception:
        QMessageBox.warning(gui,"EDIT BLOG","You must be logged in first.",)
        return

    blog = get_selected_blog(gui)
    if blog is None:
        QMessageBox.warning(gui,"EDIT BLOG","please select a blog to edit",)
        return

    # open dialog with existing blog data in place
    dlg = BlogEditDialog(
        gui,
        blog_id=str(blog.id),
        name=blog.name,
        url=blog.url,
        email=blog.email,
    )

    # dont allow changing the id
    dlg.id_edit.setEnabled(False)
    result = dlg.exec()
    if result != int(QDialog.DialogCode.Accepted): return  #cancelled

    # ignore typed id,keep blog.id
    _, name, url, email = dlg.get_values()

    # validate name
    if not name:
        QMessageBox.warning(gui, "EDIT BLOG", "blog name cannot be empty")
        return
    
    # call controller to update
    try:
        gui.controller.update_blog(blog.id, blog.id, name, url, email)
    except Exception as ex:
        QMessageBox.warning(gui,"EDIT BLOG",f"could not update blog: \n{ex}",)
        return

    QMessageBox.information(gui,"EDIT BLOG",f"Blog '{name}' (ID {blog.id}) updated successfully",)
    
    refresh_blogs(gui)
    refresh_posts(gui)



def handle_delete_blog_clicked(gui):
    """
        #delete currently selected blog after confirming

    """

    # require login
    try:
        _ = gui.controller.list_blogs()
    except Exception:
        QMessageBox.warning(gui,"DELETE BLOG","You must be logged in first.")
        return

    blog = get_selected_blog(gui)

    if blog is None:
        QMessageBox.warning(gui,"DELETE BLOG","please select a blog to delete",)
        return

    # confirm deletion
    reply = QMessageBox.question(
        gui,
        "DELETE BLOG",
        f"are you sure you want to delete blog '{blog.name}' (ID {blog.id})?\n"
        "this will remove all it posts aswell",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
    
    # user cancelled
    if reply != QMessageBox.StandardButton.Yes:return

    # delete blog
    try:
        gui.controller.delete_blog(blog.id)
    except Exception as ex:
        QMessageBox.warning(gui,"DELETE BLOG",f"could not delete blog:\n{ex}",)
        return

    QMessageBox.information(gui,"DELETE BLOG",f"Blog '{blog.name}' (ID {blog.id}) deleted")

    gui.posts_text.clear()
    refresh_blogs(gui)
    refresh_posts(gui)



def handle_new_blog_clicked(gui):
    """
        #opens dialog to create new blog, calls controller and refreshs

    """

    # require login
    try:
        _ = gui.controller.list_blogs()
    except Exception:
        QMessageBox.warning(gui,"EDIT BLOG","You must be logged in first.",)
        return

    # open dialogue
    dlg = BlogEditDialog(gui)
    result = dlg.exec()
    if result != int(QDialog.DialogCode.Accepted): return   #cancelled

    #get vals: id, name, url, email
    id_str, name, url, email = dlg.get_values()

    # validate id
    if not id_str:
        QMessageBox.warning(gui, "NEW BLOG", "Blog ID cannot be empty")
        return

    try:
        blog_id = int(id_str)
    except ValueError:
        QMessageBox.warning(gui, "NEW BLOG", "Blog ID must be an int")
        return

    # validate name
    if not name:
        QMessageBox.warning(gui, "NEW BLOG", "Blog name cannot be empty")
        return

    # call controller
    try:
        gui.controller.create_blog(blog_id, name, url, email)
    except Exception as ex:
        QMessageBox.warning(gui,"NEW BLOG",
                            f"The blog could not be created.\n"
                            f"Error details: {ex}"
                        )
        return

    QMessageBox.information(gui,"NEW BLOG",f"Blog '{name}' (ID {blog_id}) created successfully.",)

    #reload table
    refresh_blogs(gui)
    refresh_posts(gui)



def handle_search_blog_clicked(gui):
    """
    Search blogs by name substring and show results in the QTableView.

    """

    # must be logged in
    if not gui.controller.is_logged_in:
        QMessageBox.warning(gui, "SEARCH BLOG", "You must be logged in first.")
        return
    
    # get search term
    term = gui.blog_search_edit.text().strip()
    if not term:
        QMessageBox.warning(gui, "SEARCH BLOG", "Please enter a search term.")
        return
    
    # search blogs via controller
    try:
        blogs = gui.controller.retrieve_blogs(term)
    except Exception as ex:
        QMessageBox.warning(gui, "SEARCH BLOG", f"Error searching blogs:\n{ex}")
        return

    # update table with search results
    gui.blogs_model.set_blogs(blogs)
    gui.statusBar().showMessage(f"{len(blogs)} blogs found for '{term}'")
    gui.posts_text.clear()
    # clear selected blog id
    if hasattr(gui, "selected_blog_id"):
        gui.selected_blog_id = None



def handle_clear_blog_search_clicked(gui):
    """
    Clear search box and reload all blogs.
    """

    gui.blog_search_edit.clear()
    # update table to show all blogs
    refresh_blogs(gui)
    refresh_posts(gui)



################
##   posts    ##
################


def refresh_posts(gui):
    """
        #show posts for current blog in qplaintextedit

    """

    gui.posts_text.clear()

    # keep selected blog id on gui
    blog_id = getattr(gui, "selected_blog_id", None)
    if blog_id is None:return

    # fetch posts from controller
    try:
        gui.controller.set_current_blog(blog_id)    # temp make it controllers current blog
        posts = gui.controller.list_posts()

    except Exception:
        return
    
    finally:
        # clear current blog s.t update/delete not blocked
        try:
            gui.controller.unset_current_blog()
        except Exception:
            pass

    # if no posts, show a hint for user
    if not posts:
        gui.posts_text.setPlainText("No posts for this blog.")
        return

    lines = []

    for post in posts:
        # display post header
        header = f"#{post.code} - {post.title}"

        if getattr(post, "author", None): 
            header += f" (by {post.author})"

        lines.append(header)

        # display creation time if available
        created = getattr(post, "created_at", None) or getattr(post, "creation_time", None)
        if created: lines.append(f"Created: {created}")

        # display post text,
        # separated by lines
        lines.append("-" * 45)
        lines.append(post.text)
        # blank line between posts
        lines.append("-" * 20)
        lines.append("")  

    gui.posts_text.setPlainText("\n".join(lines))



def refresh_blogs(gui):
    """
        #fetch blogs from controller, show in table

    """

    try:
        blogs = gui.controller.list_blogs()
    except Exception:
        gui.blogs_model.set_blogs([])
        gui.statusBar().showMessage("unable to load blogs (are you logged in?)")
        return
    
    # sort by id
    blogs = sorted(blogs, key=lambda b: b.id)

    # update table
    gui.blogs_model.set_blogs(blogs)
    gui.statusBar().showMessage(f"{len(blogs)} blogs loaded")
    gui.posts_text.clear()



def handle_blog_selection_changed(gui, selected, deselected):
    """
        #called when user selects different blog in table

    """

    indexes = selected.indexes()
    if not indexes: return

    row = indexes[0].row()
    blog = gui.blogs_model.get_blog(row)
    if blog is None:return

    #which blog selected in gui
    gui.selected_blog_id = blog.id

    #update status, text, refresh posts
    gui.statusBar().showMessage(f"Current blog: {blog.name} (id={blog.id})")
    refresh_posts(gui)




    ################
    ##   login    ##    
    ################

def handle_login_clicked(gui):
    """
        process login attempt, update the ui, blog table on success

    """

    username = gui.username_edit.text().strip()
    password = gui.password_edit.text()
    
    if not username or not password:
        QMessageBox.warning(gui,"login","Enter both username and password",)
        return
    
    #attempt login
    try:
        ok = gui.controller.login(username, password)
    except Exception:
        ok = False

    #process result, refresh blogs on success, block login ui
    if ok:
        gui.login_status_label.setText(f"Logged in as {username}")
        gui.login_status_label.setStyleSheet("color: #66ff66; font-weight: bold;")
        gui.login_button.setEnabled(False)
        gui.logout_button.setEnabled(True)
        gui.username_edit.clear()
        gui.password_edit.clear()
        gui.username_edit.setEnabled(False)
        gui.password_edit.setEnabled(False)

        refresh_blogs(gui)

    #login failed, clear password box
    else:
        QMessageBox.warning(gui,"login","incorrect username or password",)
        gui.password_edit.clear()
        gui.password_edit.setFocus()
    





def handle_logout_clicked(gui):

    try:
        if hasattr(gui.controller, "logout"): gui.controller.logout()
    except Exception:
        pass

    # reset ui
    gui.login_status_label.setText("not logged in")
    gui.login_status_label.setStyleSheet("color: #ff6666; font-weight: bold;")
   
    # enable login ui
    gui.login_button.setEnabled(True)
    gui.logout_button.setEnabled(False)

    # enable username/password edits
    gui.username_edit.setEnabled(True)
    gui.password_edit.setEnabled(True)

    # clear blogs table and posts text
    gui.blogs_model.set_blogs([])
    gui.posts_text.clear()

    # clear username/password edits
    gui.username_edit.clear()
    gui.password_edit.clear()
    gui.username_edit.setFocus()



    ################
    ##   posts    ##
    ################


def handle_new_post_clicked(gui):
    """
        creates new post in current blog

    """

    # check login
    if not gui.controller.is_logged_in:
        QMessageBox.warning(gui, "NEW POST", "You must be logged in first.")
        return

    # check selected blog
    blog_id = getattr(gui, "selected_blog_id", None)
    if blog_id is None:
        QMessageBox.warning(gui, "NEW POST", "Please select a blog first.")
        return

    # try to set current blog
    try:
        gui.controller.set_current_blog(blog_id)
    except Exception as ex:
        QMessageBox.warning(gui, "NEW POST", f"Could not set current blog:\n{ex}")
        return

    # get title
    title, ok = QInputDialog.getText(gui, "NEW POST", "post title: ")
    if not ok or not title.strip(): return
    title = title.strip()

    # get text for post
    text, ok = QInputDialog.getMultiLineText(gui, "NEW POST", "post text: ")
    if not ok:return
    text = text.strip()

    if not text:
        QMessageBox.warning(gui, "NEW POST", "post text cannot be empty")
        return

    # try to create post via controller
    try:
        gui.controller.create_post(title, text, None)
    except Exception as ex:
        QMessageBox.warning(gui, "NEW POST", f"could not create post: \n{ex}")
        return

    QMessageBox.information(gui, "NEW POST", "post created successfully")
    refresh_posts(gui)


    
def handle_delete_post_clicked(gui):
    """
        delete a post from the current blog

    """

    # must be logged in
    if not gui.controller.is_logged_in:
        QMessageBox.warning(gui, "DELETE POST", "You must be logged in first.")
        return

    # must have selected blog
    blog_id = getattr(gui, "selected_blog_id", None)
    if blog_id is None:
        QMessageBox.warning(gui, "DELETE POST", "Please select a blog first.")
        return

    # set current blog
    try:
        gui.controller.set_current_blog(blog_id)
    except Exception as ex:
        QMessageBox.warning(gui, "DELETE POST", f"Could not set current blog:\n{ex}")
        return

    # get code to delete by user input
    code, ok = QInputDialog.getInt(gui, "DELETE POST", "post number:", min=1)
    if not ok:return

    try:
        post = gui.controller.search_post(code)
    except Exception as ex:
        QMessageBox.warning(gui, "DELETE POST", f"error looking up post:\n{ex}")
        return

    if not post:
        QMessageBox.warning(gui, "DELETE POST", "no post found with this number")
        return

    # confirm deletion
    summary = f"Post #{post.code}\ntitle: {post.title}\n\n{post.text[:200]}..."
    reply = QMessageBox.question(
        gui,
        "DELETE POST",
        f"are you sure you want to delete post?\n\n{summary}",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )

    if reply != QMessageBox.StandardButton.Yes: return

    # delete the post
    try:
        gui.controller.delete_post(code)
    except Exception as ex:
        QMessageBox.warning(gui, "DELETE POST", f"could not delete post:\n{ex}")
        return

    QMessageBox.information(gui, "DELETE POST", "post deleted")
    refresh_posts(gui)



def handle_edit_post_clicked(gui):
    """
        edit existing post in current blog

    """

    # must be logged in
    if not gui.controller.is_logged_in:
        QMessageBox.warning(gui, "EDIT POST", "You must be logged in first.")
        return

    # must have selected blog
    blog_id = getattr(gui, "selected_blog_id", None)
    if blog_id is None:
        QMessageBox.warning(gui, "EDIT POST", "Please select a blog first.")
        return

    # temp set current blog
    gui.controller.set_current_blog(blog_id)

    # ask user for post code to edit
    code, ok = QInputDialog.getInt(gui, "EDIT POST", "post number:", min=1)
    if not ok:
        return

    # check if the post exists 
    try:
        post = gui.controller.search_post(code)
    except Exception as ex:
        QMessageBox.warning(gui, "EDIT POST", f"error looking up post:\n{ex}")
        return

    if not post:
        QMessageBox.warning(gui, "EDIT POST", "no post found with this number")
        return

    # let user modify title (pre-fill old title)
    new_title, ok = QInputDialog.getText(
        gui,
        "EDIT POST",
        "new title:",
        text=post.title,
    )
    if not ok:
        return
    new_title = new_title.strip()
    if not new_title:
        QMessageBox.warning(gui, "EDIT POST", "post title cannot be empty")
        return

    # let user modify text (prefill old text)
    new_text, ok = QInputDialog.getMultiLineText(
        gui,
        "EDIT POST",
        "new text:",
        text=post.text,
    )
    if not ok:
        return
    new_text = new_text.strip()
    if not new_text:
        QMessageBox.warning(gui, "EDIT POST", "post text cannot be empty")
        return

    # update the post (prefill old text)
    try:
        updated = gui.controller.update_post(code, title=new_title, text=new_text, author=getattr(post, "author", None))
    except Exception as ex:
        QMessageBox.warning(gui, "EDIT POST", f"could not update post:\n{ex}")
        return

    if not updated:
        QMessageBox.warning(gui, "EDIT POST", "post could not be updated (maybe not found).")
        return

    QMessageBox.information(gui, "EDIT POST", "post updated successfully")
    refresh_posts(gui)



def handle_list_posts_clicked(gui):
    """
    List all posts of the currently selected blog.

    """

    # must be logged in
    if not gui.controller.is_logged_in:
        QMessageBox.warning(gui, "LIST POSTS", "You must be logged in first.")
        return

    #  must have selected blog
    blog_id = getattr(gui, "selected_blog_id", None)
    if blog_id is None:
        QMessageBox.warning(gui, "LIST POSTS", "Please select a blog first.")
        return


    # set current blog
    gui.controller.set_current_blog(blog_id)

    #   fetch posts
    try:
        posts = gui.controller.list_posts()
    except Exception as ex:
        QMessageBox.warning(gui, "LIST POSTS", f"Error retrieving posts:\n{ex}")
        return

    # clear existing text
    gui.posts_text.clear()

    # if no posts, show a hint for user
    if not posts:
        gui.posts_text.setPlainText("No posts for this blog.")
        return

    # display posts
    lines = []
    for post in posts:
        header = f"#{post.code} — {post.title}"
        if getattr(post, "author", None):
            header += f" (by {post.author})"

        lines.append(header)

        created = getattr(post, "created_at", None) or getattr(post, "creation_time", None)
        if created:
            lines.append(f"Created: {created}")

        lines.append("-" * 40)
        lines.append(post.text)
        lines.append("")  # 

    gui.posts_text.setPlainText("\n".join(lines))



