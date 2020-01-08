import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from slugify import slugify

from web.database.models import ArtpieceModel

CDIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
if not SQLALCHEMY_DATABASE_URI:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.join(CDIR, os.pardir), os.pardir))
    DB_NAME = 'ARTBot.db'
    # Put the db file in project root
    DB_PATH = os.path.join(PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

SQL_ENGINE = sa.create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=SQL_ENGINE)

@contextmanager
def session_scope():
    """Provide transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

slug_dict = dict()

with session_scope() as session:
    models = session.query(ArtpieceModel).all()
    for model in models:
        slug = slugify(model.title)
        count = (slug_dict.get(slug) or 0) + 1
        model.slug = f'{slug}-{count}'
        slug_dict[slug] = count
