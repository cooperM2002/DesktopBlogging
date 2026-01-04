


from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex




#table model to show blog objects in a qtableview
class BlogsTableModel(QAbstractTableModel):
    """
        later
    """


    def __init__(self, blogs=None, parent=None):
        
        super().__init__(parent)
        self._blogs = list(blogs) if blogs is not None else []
        self._headers = ["ID", "Name", "URL", "Email"]


    def rowCount(self, parent=QModelIndex()):
        return len(self._blogs)


    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid(): return None

        blog = self._blogs[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:return blog.id
            elif col == 1:return blog.name
            elif col == 2:return blog.url
            elif col == 3:return blog.email

        if role == Qt.ItemDataRole.TextAlignmentRole and col == 0:
            return int(
                Qt.AlignmentFlag.AlignCenter | 
                Qt.AlignmentFlag.AlignVCenter
                )   #returns int

        return None


    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
    
        if role != Qt.ItemDataRole.DisplayRole:return None
        if orientation == Qt.Orientation.Horizontal:return self._headers[section]
        else:return section + 1
        

    #replace data with new list of blog objs
    def set_blogs(self, blogs):

        self.beginResetModel()
        self._blogs = list(blogs)
        self.endResetModel()


    def get_blog(self, row):

        if 0 <= row < len(self._blogs): return self._blogs[row]
        return None