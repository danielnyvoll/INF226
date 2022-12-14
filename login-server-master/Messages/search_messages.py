from json import dumps
from apsw import Error


def searchInMessage(request,conn):
    word = request.args.get('q') or request.form.get('q')
    receiver = request.args.get('receiver') or request.form.get('receiver')
    try:
        c = conn.execute('SELECT * FROM messages WHERE message LIKE ? AND receiver = ?',(word,receiver) )
        rows = c.fetchall()
        result = 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)