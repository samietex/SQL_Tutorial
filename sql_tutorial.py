"""Run SQL straight from a notebook cell.

Load it once per notebook with ``%load_ext sql_tutorial``, then start a cell with:

- ``%%sql`` to run SQLite against the lesson database. It lives in memory, needs no
  install, and starts empty every time the notebook restarts.
- ``%%tsql`` to run T-SQL against SQL Server and the AdventureWorks2022 sample
  database. Run ``%setup_adventureworks`` once first: in Google Colab it installs
  SQL Server and AdventureWorks for you, and on your own machine it checks the
  setup from the Course Overview.

Add ``--expect-error`` after either one (``%%sql --expect-error``) for a cell that is
supposed to fail, so the lesson can show you the error without stopping the notebook.

Results show ``NULL`` exactly as a SQL client would, writes report how many rows they
touched, and errors come back as one readable line instead of a Python traceback.
"""
import base64
import html
import os
import re
import socket
import sqlite3
import subprocess
import sys
import time

from IPython.core.magic import Magics, cell_magic, line_magic, magics_class
from IPython.display import HTML, display

MAX_ROWS = 50
WRITE_VERBS = {'INSERT': 'inserted', 'UPDATE': 'updated', 'DELETE': 'deleted'}

# Colab only: SQL Server runs inside the reader's own temporary session, so a fixed
# password is fine here. It never applies to a SQL Server on someone's own machine.
COLAB_PASSWORD = 'Tutorial!Colab2026'
BACKUP_URL = 'https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorks2022.bak'


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
    rows = f"{count} row{'' if count == 1 else 's'}"
    if verb in WRITE_VERBS and count >= 0:
        return f'{rows} {WRITE_VERBS[verb]}'
    if verb == 'AFFECTED' and count >= 0:
        return f'{rows} affected'
    if verb == 'COPIED' and count >= 0:
        return f'{rows} copied'
    return None


def _tsql_write_label(batch):
    """Pick the word for a T-SQL batch's row counts.

    A batch can hold several statements but reports only bare counts, so name the verb
    only when the batch has a single write statement, and fall back to 'affected'.
    """
    text = _strip_comments(batch)
    writes = re.findall(r'(?im)^\s*(INSERT|UPDATE|DELETE)\b', text)
    if len(writes) == 1:
        return writes[0].upper()
    if not writes and re.search(r'(?is)^\s*SELECT\b.*\bINTO\s+[#\w]', text):
        return 'COPIED'
    return 'AFFECTED'


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

    @line_magic
    def setup_adventureworks(self, line):
        """Get %%tsql ready: install SQL Server and AdventureWorks in Colab, or check the local setup."""
        if _in_colab():
            _install_in_colab()
        self.server = None
        try:
            self._server()
        except Exception as exc:
            if _in_colab():
                raise SQLError(f'Error: SQL Server is installed but would not connect: {_clean_error(exc)}') from None
            print(
                'SQL Server is not reachable from this notebook yet, so the %%tsql cells will not run.\n'
                f'Reason: {_clean_error(exc)}\n'
                'Either open this notebook in Google Colab and run this cell again, which installs '
                'everything for you, or follow the "Run it on your own machine" steps in the Course '
                'Overview. The saved results under each %%tsql cell show what you would get.'
            )
            return
        print('AdventureWorks2022 is ready, so every %%tsql cell in this notebook will run.')

    @cell_magic
    def sql(self, line, cell):
        self._run(line, lambda: self._run_sqlite(cell), sqlite3.Error)

    @cell_magic
    def tsql(self, line, cell):
        self._run(line, lambda: self._run_tsql(cell), Exception)

    def _run(self, line, runner, error_type):
        expect_error = '--expect-error' in line.split()
        self.note = ''
        try:
            runner()
        except SQLError:
            raise
        except error_type as exc:
            message = _clean_error(exc) + self.note
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
        try:
            for batch in re.split(r'(?im)^\s*GO\s*$', cell):
                if not _strip_comments(batch).strip():
                    continue
                cursor.execute(batch)
                while True:
                    self._report(cursor, _tsql_write_label(batch))
                    if not cursor.nextset():
                        break
        except Exception:
            self._rollback_open_transaction()
            raise

    def _rollback_open_transaction(self):
        # A failed statement can leave a BEGIN TRANSACTION open, and every later cell would
        # then run inside it. Roll it back so one error can't quietly swallow later work.
        try:
            cursor = self.server.cursor()
            cursor.execute('SELECT @@TRANCOUNT')
            if cursor.fetchone()[0]:
                cursor.execute('ROLLBACK')
                self.note = ' (The open transaction was rolled back, so none of its changes were kept.)'
        except Exception:
            pass

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


def _in_colab():
    return 'google.colab' in sys.modules


def _port_open(port=1433):
    with socket.socket() as sock:
        sock.settimeout(1)
        return sock.connect_ex(('127.0.0.1', port)) == 0


def _shell(command, doing):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        tail = '\n'.join((result.stdout + result.stderr).strip().splitlines()[-15:])
        raise SQLError(f'Error: setup stopped while {doing}.\n{tail}')


def _install_in_colab():
    """Install SQL Server inside this Colab session and restore AdventureWorks2022 into it.

    Each step is skipped when it has already happened, so running the setup cell twice
    is quick. Colab throws the whole machine away when the session ends, which is why a
    new session needs the setup cell again.
    """
    os.environ.update(
        SQL_TUTORIAL_SERVER='localhost',
        SQL_TUTORIAL_USER='sa',
        SQL_TUTORIAL_PASSWORD=COLAB_PASSWORD,
        SQL_TUTORIAL_DATABASE='AdventureWorks2022',
    )
    started = time.time()

    if not os.path.exists('/opt/mssql/bin/sqlservr'):
        print('Step 1 of 4: installing SQL Server Developer edition (about 2 minutes)...', flush=True)
        release = re.search(r'VERSION_ID="([\d.]+)"', open('/etc/os-release').read()).group(1)
        _shell(
            'curl -fsSL https://packages.microsoft.com/keys/microsoft.asc > /etc/apt/trusted.gpg.d/microsoft.asc',
            'downloading the Microsoft signing key',
        )
        # Newer package lists expect the key unwrapped from its text armor, at a fixed path.
        armored = open('/etc/apt/trusted.gpg.d/microsoft.asc').read()
        body = armored.split('\n\n', 1)[1].split('\n=', 1)[0]
        with open('/usr/share/keyrings/microsoft-prod.gpg', 'wb') as key:
            key.write(base64.b64decode(''.join(body.split())))
        # Microsoft publishes SQL Server 2022 up to Ubuntu 22.04 and 2025 from 22.04 on.
        # Either one restores the AdventureWorks2022 backup and runs every query in the course.
        lists = ' '.join(
            f'https://packages.microsoft.com/config/ubuntu/{release}/mssql-server-{year}.list'
            for year in ('2022', '2025')
        )
        _shell(
            f'for url in {lists}; do curl -fsSL "$url" > /etc/apt/sources.list.d/mssql-server.list && break; done; '
            'test -s /etc/apt/sources.list.d/mssql-server.list && '
            'apt-get update -q && DEBIAN_FRONTEND=noninteractive apt-get install -y -q mssql-server',
            f'installing SQL Server on Ubuntu {release}',
        )
    else:
        print('Step 1 of 4: SQL Server is already installed.', flush=True)

    try:
        import pymssql
    except ImportError:
        _shell(f'{sys.executable} -m pip install -q pymssql', 'installing pymssql')
        import pymssql

    if not _port_open():
        print('Step 2 of 4: starting SQL Server...', flush=True)
        _shell('mkdir -p /var/opt/mssql/backup && chown -R mssql:mssql /var/opt/mssql', 'preparing folders')
        env = dict(os.environ, ACCEPT_EULA='Y', MSSQL_PID='Developer',
                   MSSQL_SA_PASSWORD=COLAB_PASSWORD, MSSQL_MEMORY_LIMIT_MB='4096')
        with open('/tmp/sqlservr.log', 'w') as log:
            subprocess.Popen(['runuser', '-u', 'mssql', '--', '/opt/mssql/bin/sqlservr'],
                             env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    else:
        print('Step 2 of 4: SQL Server is already running.', flush=True)

    conn = None
    for _ in range(90):
        try:
            conn = pymssql.connect(server='localhost', user='sa', password=COLAB_PASSWORD, database='master')
            break
        except pymssql.Error:
            time.sleep(2)
    if conn is None:
        tail = '\n'.join(open('/tmp/sqlservr.log').read().strip().splitlines()[-15:])
        raise SQLError(f'Error: SQL Server did not start within 3 minutes. Its log ends with:\n{tail}')
    conn.autocommit(True)
    cursor = conn.cursor()

    cursor.execute("SELECT DB_ID('AdventureWorks2022')")
    if cursor.fetchone()[0] is None:
        print('Step 3 of 4: downloading the AdventureWorks2022 backup (about 50 MB)...', flush=True)
        backup = '/var/opt/mssql/backup/AdventureWorks2022.bak'
        _shell(f'curl -fsSL -o {backup} {BACKUP_URL} && chown mssql:mssql {backup}', 'downloading AdventureWorks')
        print('Step 4 of 4: restoring AdventureWorks2022 into SQL Server...', flush=True)
        cursor.execute(f"RESTORE FILELISTONLY FROM DISK = '{backup}'")
        # The backup records Windows file paths, so each file is moved into SQL Server's Linux data folder.
        moves = ', '.join(
            f"MOVE '{name}' TO '/var/opt/mssql/data/{path.replace(chr(92), '/').rsplit('/', 1)[-1]}'"
            for name, path, *_ in cursor.fetchall()
        )
        cursor.execute(f"RESTORE DATABASE AdventureWorks2022 FROM DISK = '{backup}' WITH {moves}, RECOVERY")
        while cursor.nextset():
            pass
    else:
        print('Steps 3 and 4: AdventureWorks2022 is already restored.', flush=True)
    conn.close()
    print(f'Finished in {time.time() - started:.0f} seconds.', flush=True)


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
    if _in_colab():
        raise SQLError(
            'Error: this cell runs on SQL Server, which Colab does not include. Run the '
            '%setup_adventureworks cell at the start of the AdventureWorks section first; it '
            'installs SQL Server for this session in a few minutes.'
        )
    raise SQLError(
        'Error: no SQL Server connection is configured. Either install the Microsoft ODBC Driver '
        'for SQL Server and pip install pyodbc (Windows login works then), or set '
        'SQL_TUTORIAL_USER and SQL_TUTORIAL_PASSWORD. The Course Overview walks through both.'
    )


def load_ipython_extension(ipython):
    ipython.register_magics(SQLTutorialMagics)
    print(f'Ready. %%sql runs SQLite {sqlite3.sqlite_version} in memory, %%tsql runs SQL Server.')
