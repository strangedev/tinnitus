========
tinnitus
========
Tinnitus is a media player and playback queue.
It comes in two parts, service and remote. Once the *tinnitusd* service is running, the Python remote can be used to manipulate the queue and control playback.
Tinnitus is *thread-safe*, meaning it can be accessed by any number of processes at once.

Setup
^^^^^
Install *tinnitusd* via setuptools. In most cases, you'll want to use *virtualenv*.

``git clone https://github.com/strangedev/tinnitus.git``

``cd tinnitus``

Optional: ``virtualenv .tinnitus``

Optional: ``. .tinnitus/bin/activate``

``pip install -e .``

You can now run the service in your virtualenv with ``tinnitusd [port]``.


Remote
^^^^^^
To use the remote, first install tinnitus into the virtualenv you're using for your project, as described above.

You can then ``from tinnitus import remote`` and use the contextmanager to talk to the service:

``with remote() as r:``

``print(r.status())``

To use a different port than the default host or port, use ``tinnitus.configure(host, port)`` before using the remote.