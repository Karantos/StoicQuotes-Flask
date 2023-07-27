"""
This script runs the application using a development server.
"""

from website import create_app

app = create_app()

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
