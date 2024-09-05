from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, ComboBox

from ok.gui.Communicate import communicate
from ok.gui.util.Alert import alert_error
from ok.logging.Logger import get_logger
from ok.update.GitUpdater import GitUpdater

logger = get_logger(__name__)


class RunBar(QWidget):

    def __init__(self, updater: GitUpdater):
        super().__init__()

        self.updater = updater

        self.layout = QHBoxLayout()
        self.update_source = ComboBox()
        self.layout.addWidget(self.update_source)
        communicate.versions.connect(self.update_versions)
        communicate.clone_version.connect(self.clone_version)

        self.version_list = ComboBox()
        self.layout.addWidget(self.version_list)

        self.check_update_button = PushButton(self.tr("Check for Update"))
        self.layout.addWidget(self.check_update_button)

        self.update_button = PushButton(self.tr("Update"))
        self.update_button.clicked.connect(self.update_clicked)
        self.layout.addWidget(self.update_button)

        self.run_button = PushButton(self.tr("Run"))
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)

        self.updater.list_all_versions()

    def update_clicked(self):
        self.updater.update_to_version(self.version_list.currentText())
        self.update_button.setDisabled(True)

    def clone_version(self, error):
        self.update_button.setDisabled(False)
        if error:
            alert_error(error)

    def update_versions(self, versions):
        if versions is None:  # fetch version error
            self.version_list.clear()
        else:
            current_items = [self.version_list.itemText(i) for i in range(self.version_list.count())]
            if current_items != versions:
                self.version_list.clear()
                self.version_list.addItems(versions)
