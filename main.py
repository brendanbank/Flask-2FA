""" 

© 2020 Brendan Bank <brendan.bank@gmail.com>

"""

from example import create_app

app = create_app()

if __name__ == "__main__":
    # Only for debugging while developing

    app.run(host='0.0.0.0', debug=True, ssl_context='adhoc', port=5000)
