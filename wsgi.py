from app import create_app

from settings import Settings


if __name__ == "__main__":
    app = create_app()
    app.run(host=Settings.HOST, port=Settings.PORT, debug=Settings.DEBUG)
