from json import dumps
from apsw import Error


def searchInMessage(request,conn):
    query = request.args.get('q') or request.form.get('q') or '*'
    stmt = f"SELECT * FROM messages WHERE message GLOB '{query}'"
    try:
        c = conn.execute(stmt)
        rows = c.fetchall()
        result = 'Result:\n'
        for row in rows:
            result = f'{result}    {dumps(row)}\n'
        c.close()
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)