from laigui.gui import LAIGUIApp

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LAIGUIApp()
    window.show()
    sys.exit(app.exec_())
