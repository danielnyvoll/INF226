from apsw import Error
from flask import escape
from json import dumps
from apsw import Error


def getMessages(request,conn):
    receiver = request.args.get('q') or request.form.get('q')
    try:
        c = conn.execute('SELECT * FROM messages WHERE receiver = ?',(receiver,))
        rows = c.fetchall()
        result = 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)