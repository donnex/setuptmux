#!/usr/bin/env python
import sys
from pbs import tmux

sessions = {
    'system': (
        ('messages', 'clear; tail -F /var/log/messages'),
        ('logwatch', 'clear; logwatch'),
        ('top', 'top'),
     ),
}


# Session argument
if len(sys.argv) != 2:
    sys.exit('Error: Missing session name')

# Session name
session_name = sys.argv[1]
session = sessions.get(session_name)
if not session:
    sys.exit('Error: Invalid session name')

# Setup tmux
tmux('-2', 'new-session', '-d', '-s', session_name, _fg=True)
for i, session in enumerate(session):
    window_name, window_cmd = session
    tmux('new-window', '-t', '%s:%d' % (session_name, i), '-k', '-n %s' % (window_name,), _fg=True)
    tmux('send-keys', '-t', '%s:%d' % (session_name, i), window_cmd, 'C-m', _fg=True)
tmux('select-window', '-t', '%s:0' % (session_name,))

# Done
print('%s tmux setup completed' % (session_name,))
