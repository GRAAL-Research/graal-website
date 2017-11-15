import logging
import sys

from graal import app as application


logging.basicConfig(stream=sys.stderr)


if __name__ == "__main__":
    app.run()
