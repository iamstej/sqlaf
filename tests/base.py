from unittest import TestCase

import sqlalchemy

from tests.implementation.db import Session, engine


class FilterTestCase(TestCase):
    def setUp(self):
        self.session = Session()

    def tearDown(self):
        self.session.rollback()

        inspector = sqlalchemy.inspect(engine)

        for tbl in inspector.get_table_names():
            if "alembic" not in tbl:
                self.session.execute('TRUNCATE TABLE "{}" CASCADE'.format(tbl))

        self.session.commit()
        self.session.expunge_all()
