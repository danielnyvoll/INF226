import datetime
from apsw import Error

def sendMessage(request,conn):
    try:
        sender = request.args.get('sender') or request.form.get('sender')
        message = request.args.get('message') or request.form.get('message')
        receiver = request.args.get('receiver') or request.form.get('receiver')
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(time)
        if not sender:
            return f'ERROR: missing sender'
        if not message:
            return f'ERROR: missing message'
        if not receiver:
            return f'ERROR: missing receiver'
        conn.execute('INSERT INTO messages (sender, message, receiver, time) VALUES (?, ?, ?, ?)', (sender, message, receiver, time))
        return f'Message sent!'
    except Error as e:
        return f'ERROR: {e}'
    