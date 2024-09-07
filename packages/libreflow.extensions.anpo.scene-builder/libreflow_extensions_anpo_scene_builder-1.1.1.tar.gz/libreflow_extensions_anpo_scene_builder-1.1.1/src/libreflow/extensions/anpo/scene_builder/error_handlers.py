import os
import re
import uuid
from kabaret import flow
from kabaret.flow_entities.entities import EntityCollection, Entity, Property


class RemoveHandler(flow.Action):
    ICON = ('icons.gui', 'remove-symbol')
    _handler = flow.Parent()
    _handlers = flow.Parent(2)

    def needs_dialog(self):
        return False

    def run(self, button):
        handlers = self._handlers
        handlers.delete_entities([self._handler.name()])
        handlers.touch()

class ErrorHandler(Entity):
    description = Property()
    pattern = Property().ui(editor='textarea')
    whence = Property().ui(editor='int')
    runner = Property()
    enabled = Property().ui(editor='bool')
    remove = flow.Child(RemoveHandler)

    def match(self, log_path):
        '''
        Check if the content of the given log file matches the
        handler's error pattern.

        The matching is performed on the last `whence` bytes of
        the file. The function returns the error message matched
        by the pattern. If the latter contains groups, the string
        will be a concatenation of these separated by `\n`.

        :param log_path: the path to a process log file
        :type log_path: str
        :return: the caught error message
        :rtype: str
        '''
        whence = min(os.path.getsize(log_path), self.whence.get()) # limit whence position according to log file size
        with open(log_path, 'rb') as f_log:
            f_log.seek(-whence, 2)
            log = f_log.read().decode('utf-8')
        m = re.search(self.pattern.get(), log)
        if m is None:
            return None

        groups = m.groups()
        if not groups:
            return m.string[m.start():m.end()]

        return '\n'.join(m.groups())

class RunnerName(flow.values.SessionValue):
    DEFAULT_EDITOR = 'choice'

    def choices(self):
        runners = self.root().project().get_factory().find_runners()
        return [r[0] for r in runners]

    def revert_to_defaul(self):
        names = self.choices()
        if names:
            self.set(names[0])

class AddErrorHandler(flow.Action):
    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')
    description = flow.SessionParam("")
    pattern = flow.SessionParam("").ui(editor='textarea')
    whence = flow.SessionParam(200).ui(
        tooltip="Number of last bytes used to search for errors")
    runner = flow.SessionParam(None, RunnerName)
    _handlers = flow.Parent()

    def needs_dialog(self):
        self.runner.revert_to_default()
        return True

    def get_buttons(self):
        return ['Add', 'Cancel']

    def run(self, button):
        if button == 'Cancel':
            return

        _id = f"h{uuid.uuid4().hex}"
        self._handlers.ensure_exist([_id])
        self._handlers.touch()
        handler = self._handlers[_id]
        handler.pattern.set(self.pattern.get())
        handler.whence.set(self.whence.get())
        handler.description.set(self.description.get())
        handler.runner.set(self.runner.get())
        handler.enabled.set(True)
        self._handlers.touch()

class ErrorHandlers(EntityCollection):
    add_handler = flow.Child(AddErrorHandler)

    @classmethod
    def mapped_type(cls):
        return ErrorHandler

    def columns(self):
        return ['Description', 'Application']

    def get_handlers(self, runner_name=None):
        '''
        Return enabled error handlers associated to the given
        runner name. If `runner_name` is `None`, all enabled
        handlers are returned.
        '''
        _filter = {'enabled': True}
        if runner_name is not None:
            _filter['runner'] = runner_name
        coll = self.get_entity_store().get_collection(self.collection_name())
        handlers = [self.get_mapped(d['name']) \
            for d in coll.find(_filter)]
        return handlers

    def _fill_row_cells(self, row, item):
        row['Description'] = item.description.get()
        row['Application'] = item.runner.get()

    def _fill_row_style(self, style, item, row):
        icon = ('icons.gui', 'check')
        if not item.enabled.get():
            icon = ('icons.gui', 'check-box-empty')
        style['icon'] = icon
