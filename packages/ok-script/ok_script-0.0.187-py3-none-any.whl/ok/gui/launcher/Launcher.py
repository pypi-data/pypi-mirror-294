from ok.gui.launcher.LauncherWindow import LauncherWindow
from ok.gui.util.app import init_app_config, center_window
from ok.util.exit_event import ExitEvent


class Launcher:

    def __init__(self, config):
        self.app = None
        self.locale = None
        self.config = config
        self.exit_event = ExitEvent()

    def start(self):
        self.app, self.locale = init_app_config()

        w = LauncherWindow(self.config, self.exit_event)
        center_window(self.app, w)
        w.show()
        self.app.exec_()
