from app import app, db

from config import *


def main():
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(host=HOST, port=PORT)


if __name__ == '__main__':
    main()
