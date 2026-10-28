"""Run SQL straight from a notebook cell.

Load it once per notebook with ``%load_ext sql_tutorial``, then start a cell with:

- ``%%sql`` to run SQLite against the lesson database. It lives in memory, needs no
  install, and starts empty every time the notebook restarts.
- ``%%tsql`` to run T-SQL against SQL Server and the AdventureWorks2022 sample
  database. See the Course Overview for how to set that up.

Add ``--expect-error`` after either one (``%%sql --expect-error``) for a cell that is
supposed to fail, so the lesson can show you the error without stopping the notebook.

Results show ``NULL`` exactly as a SQL client would, writes report how many rows they
touched, and errors come back as one readable line instead of a Python traceback.
"""
import html
import os
import re
import sqlite3
import sys

from IPython.core.magic import Magics, cell_magic, line_magic, magics_class
from IPython.display import HTML, display

MAX_ROWS = 50
WRITE_VERBS = {'INSERT': 'inserted', 'UPDATE': 'updated', 'DELETE': 'deleted'}


class SQLError(Exception):
    """A database error, shown as one readable line instead of a Python traceback."""

    def _render_traceback_(self):
        return [str(self)]


class Result:
    """One result set, rendered as a table in both HTML and plain text."""

    def __init__(self, columns, rows):
        self.columns = columns
        self.total = len(rows)
        self.rows = [[_show(value) for value in row] for row in rows[:MAX_ROWS]]

    def _footer(self):
        if self.total > MAX_ROWS:
            return f'Showing the first {MAX_ROWS} of {self.total:,} rows.'
        return f"{self.total} row{'' if self.total == 1 else 's'}"

    def _repr_html_(self):
        head = ''.join(f'<th>{html.escape(c)}</th>' for c in self.columns)
        body = ''.join(
            '<tr>' + ''.join(
                '<td><i>NULL</i></td>' if is_null else f'<td>{html.escape(v)}</td>'
                for v, is_null in row
            ) + '</tr>'
            for row in self.rows
        )
        return f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table><p><small>{self._footer()}</small></p>'

    def __repr__(self):
        cells = [list(self.columns)] + [[v for v, _ in row] for row in self.rows]
        widths = [max(len(r[i]) for r in cells) for i in range(len(self.columns))]
        line = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'

        def fmt(r):
            return '| ' + ' | '.join(v.ljust(w) for v, w in zip(r, widths)) + ' |'

        out = [line, fmt(cells[0]), line] + [fmt(r) for r in cells[1:]] + [line, self._footer()]
        return '\n'.join(out)


def _show(value):
    # Pair each shown value with whether it was a real NULL, so a text value 'NULL' stays plain.
    if value is None:
        return ('NULL', True)
    if isinstance(value, float) and value.is_integer():
        return (f'{value:.1f}', False)
    return (str(value), False)


def _split_sqlite(sql):
    """Split a SQLite script into statements, respecting semicolons inside strings."""
    statements, buffer = [], ''
    for part in sql.split(';'):
        buffer += part + ';'
        if sqlite3.complete_statement(buffer):
            statements.append(buffer)
            buffer = ''
    if buffer.strip(' \n\t;'):
        statements.append(buffer)
    return [s for s in statements if _strip_comments(s).strip(' \n\t;')]


def _strip_comments(sql):
    return re.sub(r'--[^\n]*|/\*.*?\*/', '', sql, flags=re.S)


def _write_message(statement, count):
    verb = _strip_comments(statement).split(None, 1)[0].upper()
    if verb in WRITE_VERBS and count >= 0:
        return f"{count} row{'' if count == 1 else 's'} {WRITE_VERBS[verb]}"
    return None


@magics_class
class SQLTutorialMagics(Magics):

    def __init__(self, shell):
        super().__init__(shell)
        self.lesson_db = self._new_lesson_db()
        self.server = None

    @staticmethod
    def _new_lesson_db():
        # isolation_level=None keeps SQLite's own autocommit behavior, so BEGIN and
        # ROLLBACK in a lesson do exactly what they would in the sqlite3 command line.
        return sqlite3.connect(':memory:', isolation_level=None)

    @line_magic
    def sql_reset(self, line):
        """Throw away the lesson database and start again from empty."""
        self.lesson_db.close()
        self.lesson_db = self._new_lesson_db()
        print('Lesson database reset. It is empty now, run the setup cell again.')

    @line_magic
    def tsql_connect(self, line):
        """Connect %%tsql to SQL Server. Settings come from SQL_TUTORIAL_* environment variables."""
        self.server = None
        self._server()
        print(f"Connected to SQL Server, database {os.environ.get('SQL_TUTORIAL_DATABASE', 'AdventureWorks2022')}.")

    @cell_magic
    def sql(self, line, cell):
        self._run(line, lambda: self._run_sqlite(cell), sqlite3.Error)

    @cell_magic
    def tsql(self, line, cell):
        self._run(line, lambda: self._run_tsql(cell), Exception)

    def _run(self, line, runner, error_type):
        expect_error = '--expect-error' in line.split()
        try:
            runner()
        except SQLError:
            raise
        except error_type as exc:
            message = _clean_error(exc)
            if expect_error:
                print(f'Error (this cell is meant to fail): {message}', file=sys.stderr)
                return
            raise SQLError(f'Error: {message}') from None
        if expect_error:
            raise SQLError('This cell was expected to fail, but it ran without an error.')

    def _run_sqlite(self, cell):
        for statement in _split_sqlite(cell):
            cursor = self.lesson_db.execute(statement)
            self._report(cursor, statement)

    def _run_tsql(self, cell):
        cursor = self._server().cursor()
        for batch in re.split(r'(?im)^\s*GO\s*$', cell):
            if not _strip_comments(batch).strip():
                continue
            cursor.execute(batch)
            while True:
                self._report(cursor, batch)
                if not cursor.nextset():
                    break

    def _report(self, cursor, statement):
        if cursor.description:
            columns = [c[0] for c in cursor.description]
            display(Result(columns, cursor.fetchall()))
        else:
            message = _write_message(statement, cursor.rowcount)
            if message:
                print(message)

    def _server(self):
        if self.server is None:
            self.server = _connect_sql_server()
        return self.server


def _clean_error(exc):
    text = str(exc.args[1] if len(exc.args) > 1 and isinstance(exc.args[1], str) else exc)
    # Drivers prefix SQL Server messages with codes and driver names nobody needs to read.
    text = re.sub(r'^\(?\'?\d{5}\'?,?\s*', '', text)
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\s*\(\d+\)\s*\(SQL\w+\)', '', text)
    return ' '.join(text.split()).strip(' "\'()')


def _connect_sql_server():
    """Connect with a username and password if one is set, otherwise with Windows login."""
    server = os.environ.get('SQL_TUTORIAL_SERVER', 'localhost')
    database = os.environ.get('SQL_TUTORIAL_DATABASE', 'AdventureWorks2022')
    user = os.environ.get('SQL_TUTORIAL_USER')
    password = os.environ.get('SQL_TUTORIAL_PASSWORD')
    try:
        import pyodbc
    except ImportError:
        pyodbc = None
    if pyodbc is not None:
        drivers = [d for d in pyodbc.drivers() if 'ODBC Driver' in d and 'SQL Server' in d]
        if drivers:
            login = f'UID={user};PWD={password}' if user else 'Trusted_Connection=yes'
            return pyodbc.connect(
                f'DRIVER={{{sorted(drivers)[-1]}}};SERVER={server};DATABASE={database};'
                f'{login};TrustServerCertificate=yes',
                autocommit=True,
            )
    if user:
        try:
            import pymssql
        except ImportError:
            raise SQLError('Error: install pymssql (pip install pymssql) to connect to SQL Server.') from None
        host, _, port = server.partition(',')
        conn = pymssql.connect(server=host, port=port or '1433', user=user, password=password, database=database)
        conn.autocommit(True)
        return conn
    raise SQLError(
        'Error: no SQL Server connection is configured. Either install the Microsoft ODBC Driver '
        'for SQL Server and pip install pyodbc (Windows login works then), or set '
        'SQL_TUTORIAL_USER and SQL_TUTORIAL_PASSWORD. The Course Overview walks through both.'
    )


def load_ipython_extension(ipython):
    ipython.register_magics(SQLTutorialMagics)
    print(f'Ready. %%sql runs SQLite {sqlite3.sqlite_version} in memory, %%tsql runs SQL Server.')
