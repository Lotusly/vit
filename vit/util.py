import os
import sys
import curses
import shlex

from urwid.util import calc_width

curses.setupterm()
e3_seq = curses.tigetstr('E3') or b''
clear_screen_seq = curses.tigetstr('clear') or b''

def clear_screen():
    os.write(sys.stdout.fileno(), e3_seq + clear_screen_seq)

def string_to_args(string):
    """Split like a POSIX shell when possible (quoted phrases, escapes).

    If quotes are unbalanced (e.g. apostrophe in it's, or 3\" in a size),
    shlex raises ValueError; fall back to splitting on whitespace so the
    line still reaches task(1) as separate argv tokens instead of failing
    silently with no arguments.
    """
    try:
        return shlex.split(string)
    except ValueError:
        return string.split()


def string_to_args_for_task_add(text):
    """Split a task(1) ``add`` line into argv tokens after ``task add``.

    Uses non-POSIX shlex so straight apostrophes (it's) and inch marks (3\")
    are not treated as shell quotes, while tokens like +tag and project:x
    still split on whitespace. If shlex still fails, fall back to str.split().
    """
    try:
        return shlex.split(text, posix=False)
    except ValueError:
        return text.split()


def string_to_args_for_task_modify(text):
    """Split a ``task <id> modify`` argument line.

    POSIX shlex preserves quoted phrases and +tag due:tomorrow style lists.
    On unbalanced quotes, pass the whole line as one argv token so values
    like desc:it's ok are not broken across tokens.
    """
    try:
        return shlex.split(text)
    except ValueError:
        stripped = text.strip()
        return [stripped] if stripped else []

def string_to_args_on_whitespace(string):
    try:
        lex = shlex.shlex(string)
        lex.whitespace_split = True
        return list(lex)
    except ValueError:
        return string.split()

def is_mouse_event(key):
    return not isinstance(key, str)

def uuid_short(uuid):
    return uuid[0:8]

def task_id_or_uuid_short(task):
    return task['id'] or uuid_short(task['uuid'])

def task_pending(task):
    return task['status'] == 'pending'

def task_completed(task):
    return task['status'] == 'completed' or task['status'] == 'deleted'

def project_get_subproject_and_parents(project):
    parts = project.split('.')
    subproject = parts.pop()
    parents = parts if len(parts) > 0 else None
    return subproject, parents

def project_get_root(project):
    return project.split('.')[0] if project else None

def file_to_class_name(file_name):
    words = file_name.split('_')
    return ''.join((w.capitalize() for w in words))

def file_readable(filepath):
    return os.path.isfile(filepath) and os.access(filepath, os.R_OK)

def unicode_len(string):
    return calc_width(string, 0, len(string))
