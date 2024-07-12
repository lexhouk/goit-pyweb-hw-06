from logging import WARNING, basicConfig, warning
from sqlite3 import Cursor, Error, connect


class Table:
    def __init__(self, cursor: Cursor, name: str, column: str) -> None:
        cursor.execute('DROP TABLE IF EXISTS ' + name)

        query = f'''
            CREATE TABLE {name}
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {column} VARCHAR(100) UNIQUE NOT NULL
            )
        '''

        cursor.execute(query)

        cursor.executemany(f'INSERT INTO {name} ({column}) VALUES (?)',
                           [(f'{name[:-1].title()}  #{id + 1}',)
                            for id in range(5)])


def main() -> None:
    basicConfig(level=WARNING)

    with connect('db.sqlite') as connection:
        cursor = connection.cursor()

        for name in ('students', 'groups', 'teachers', 'subjects', 'grades'):
            Table(cursor, name, 'value' if name == 'grades' else 'name')

        try:
            connection.commit()
        except Error as e:
            warning(e)

        cursor.close()


if __name__ == '__main__':
    main()
