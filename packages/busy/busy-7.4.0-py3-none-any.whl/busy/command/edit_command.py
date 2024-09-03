

from busy.command import CollectionCommand
from busy.util.edit import edit_items


class EditorCommandBase(CollectionCommand):

    selection_optional = True

    @CollectionCommand.wrap
    def execute(self):
        command = self.app.config.get('editor') or 'emacs'
        edited = edit_items(self.collection,
                            self.selection, command)
        self.status = f"Edited {self.summarize(edited)}"


class EditOneItemCommand(EditorCommandBase):
    """Edit items; default to just one"""

    name = "edit"


class EditManyCommand(EditorCommandBase):
    """Edit items; default to all"""

    name = 'manage'
    default_filter = ["1-"]
