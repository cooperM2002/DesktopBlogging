


from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
)


class BlogEditDialog(QDialog):
    """
        later
    """

    def __init__(
            self, 
            parent=None, 
            blog_id: str = "", 
            name: str = "", url: 
            str = "", email: 
            str = ""
        ):
        super().__init__(parent)


        self.setWindowTitle("New Blog")


        layout = QFormLayout(self)

        
        self.id_edit = QLineEdit(blog_id)
        self.name_edit = QLineEdit(name)
        self.url_edit = QLineEdit(url)
        self.email_edit = QLineEdit(email)


        layout.addRow("ID:", self.id_edit)
        layout.addRow("Name:", self.name_edit)
        layout.addRow("URL:", self.url_edit)
        layout.addRow("Email:", self.email_edit)


        buttons = QDialogButtonBox( 
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )


        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)


        layout.addRow(buttons)



    def get_values(self) -> tuple[str, str, str, str]:
        return (
            self.id_edit.text().strip(),
            self.name_edit.text().strip(),
            self.url_edit.text().strip(),
            self.email_edit.text().strip(),
        )