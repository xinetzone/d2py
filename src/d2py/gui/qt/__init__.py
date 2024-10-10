try:
    from .qt5 import QtCore, QtGui, QtWidgets, Signal, Slot, QtPrintSupport, QtQml
except:
    from .qt6 import QtCore, QtGui, QtWidgets, Signal, Slot, QtPrintSupport, QtQml