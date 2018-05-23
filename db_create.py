from app import create_app
from core import db
from model import *


def main():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


if __name__ == '__main__':
    main()
