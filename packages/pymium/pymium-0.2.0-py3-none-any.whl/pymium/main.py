
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtCore
import sys

from typing import Optional,Self, List

html_base = """{$using pymium}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{$title}</title>
</head>
{$space}
</html>"""

class ElementType:
    def __init__(self,
                 name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

class Style:
    def __init__(self, **styles) -> None:
        self.styles = styles

    def add_style(self, **styles):
        self.styles = self.styles | styles

    def clone(self) -> Self:
        return Style(**self.styles)
        
    def __str__(self) -> None | str:
        if not self.styles:
            return ""
        results = ""
        for key in self.styles.keys():
            results += key.replace("_","-") + ":" + self.styles[key] + ";"
        return results

class Types:
    div = ElementType("div")
    p = ElementType("p")
    h1 = ElementType("h1")
    h2 = ElementType("h2")
    h3 = ElementType("h3")
    h4 = ElementType("h4")
    h5 = ElementType("h5")
    h6 = ElementType("h6")
    button = ElementType("button")

class Space:
    def __init__(self, title: str, style: Optional[Style] = None) -> None:
        self._elements: List[Element] = list()
        self.style = style or Style()
        self.title= title
    
    @property
    def elements(self):
        return self._elements

    def append(self, Element):
        self._elements.append(Element)
    
    def _wrap_with_string(self, text: str) -> str:
        return f'"{text}"'
    
    def __str__(self) -> str:
        result: str = ""

        result = html_base.replace("{$space}", f"<body {' style = ' + self._wrap_with_string(str(self.style)) if str(self.style) else ''}>{''.join([str(element) for element in self._elements])}</body>").replace("{$using pymium}", "").replace("{$title}", self.title)
        return result

class Element:
    def __init__(self,
                 elementType: ElementType,
                 id: Optional[str] = None,
                 className: Optional[str] = None,
                 innerHTML: Optional[str] = None,
                 style: Optional[Style] = None
                 ):
        self.elementType = elementType
        self.id = id
        self.className = className
        self.innerHTML = innerHTML
        self.style = style or Style()
        self._parent: Optional[Self] = None
        self._childs: list[Self] = []

    @property
    def parent(self) -> Optional[Self]:
        return self._parent
    
    @parent.setter
    def parent(self, parent:Self):
        self._parent = parent

    @property
    def childs(self) -> list[Self]:
        return self._childs
    
    def append(self, *elements: Self) -> None:
        for element in elements:
            element.parent = self.__class__
            self._childs.append(element)
    
    def _wrap_with_string(self, text: str) -> str:
        return f'"{text}"'

    def __str__(self):
        return f"<{self.elementType}{' class = ' + self._wrap_with_string(self.className) if self.className else ''}{' id = ' + self._wrap_with_string(self.id) if self.id else ''}{' style = ' + self._wrap_with_string(str(self.style)) if str(self.style) else ''}>{self.innerHTML if self.innerHTML else ''}{''.join([str(element) for element in self._childs])}</{self.elementType}>"

def getElementById(space: Space, id: str) -> list:
    results = list()

    return _find_in_list_by_id(space.elements, id)

def _find_in_list_by_id(choosen_list: list, id: str) -> list:
    results = list()

    for element in choosen_list:
        if type(element) == list:
            results = results + _find_in_list_by_id(element, id)
            continue

        if element.id == id:
            results.append(element)
    return results

class _MainWindow(QMainWindow):
    def __init__(self, space: Space, title: str, width: int = 800, height: int = 600, frameless: bool = False, on_top: bool = False):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        view = QtWebEngineWidgets.QWebEngineView()
        html = str(space)
        view.setHtml(html)
        self.setWindowFlags(
            self.windowFlags() 
            | QtCore.Qt.FramelessWindowHint if frameless else self.windowFlags() 
            | QtCore.Qt.WindowStaysOnTopHint if on_top else self.windowFlags() 
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        
        # self.setWindowOpacity(0.5)
        self.setCentralWidget(view)

def run(space:Space, width: int = 800, height: int = 600, always_on_top: bool = False, frameless: bool= False):
    app = QApplication(sys.argv)


    window = _MainWindow(space, space.title, width, height, frameless, always_on_top)
    window.show()


    app.exec()