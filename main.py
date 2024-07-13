from logging import WARNING, basicConfig, warning
from pathlib import Path
from pprint import pprint
from random import randint
from re import search, sub
from sqlite3 import Cursor, Error, connect

from faker import Faker

STUDENTS = randint(30, 50)
SUBJECTS = randint(5, 8)

fake = Faker()


def grades() -> list[tuple]:
    results = []

    for student in range(1, STUDENTS + 1):
        for _ in range(randint(0, 20)):
            results.append((randint(0, 100), student, randint(1, SUBJECTS)))

    return results


TABLES = {
    'groups': {
        'type': 'CHAR(5) UNIQUE',
        'value': lambda: '{}-{}{}'.format(
            # Two-letter abbreviation of the name of the specialty.
            sub(r'[^A-Z]', '', fake.name())[:2],
            # Academic year number.
            randint(1, 5),
            # Serial number of the group of students in the educational stream.
            randint(1, 3)
        ),
        'rows': 3
    },
    'students': {
        'relations': ('groups',),
        'rows': STUDENTS
    },
    'teachers': {
        'rows': randint(3, 5)
    },
    'subjects': {
        'relations': ('teachers',),
        'value': lambda: fake.job(),
        'rows': SUBJECTS
    },
    'grades': {
        'relations': ('students', 'subjects'),
        'column': 'value',
        'type': 'TINYINT UNSIGNED',
        'rows': grades
    }
}


def table(cursor: Cursor, name: str) -> None:
    cursor.execute(f'DROP TABLE IF EXISTS {name}')

    column = TABLES[name].get('column', 'name')
    type = TABLES[name].get('type', 'VARCHAR(100) UNIQUE')
    columns = {column: f'{type} NOT NULL'}
    constraints = []
    relations = TABLES[name].get('relations', ())

    for relation in relations:
        columns[f'{relation[:-1]}_id'] = 'INTEGER'

        constraints.append(f'''FOREIGN KEY ({relation[:-1]}_id)
                            REFERENCES {relation} (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE''')

    query = f'''
        CREATE TABLE {name}
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {",".join(f"{key} {value}" for key, value in columns.items())}
            {"," if constraints else ""}
            {",".join(constraints)}
        )
    '''

    cursor.execute(query)

    query = f'''
        INSERT INTO {name} ({",".join(columns.keys())})
        VALUES ({",".join(["?" for _ in range(len(columns))])})
    '''

    if isinstance(TABLES[name]['rows'], int):
        sequence = [
            (
                TABLES[name].get('value', fake.name)(),
                *[randint(1, TABLES[relation]['rows'])
                  for relation in relations]
            )
            for _ in range(TABLES[name]['rows'])
        ]
    else:
        sequence = TABLES[name]['rows']()

    cursor.executemany(query, sequence)


def main() -> None:
    basicConfig(level=WARNING)

    with connect('db.sqlite') as connection:
        cursor = connection.cursor()

        [table(cursor, name) for name in TABLES.keys()]

        ids = [int(result.group(1))
               for path in Path('.').glob('query_*.sql')
               if (result := search(r'^query_(\d+)\.sql$', path.name))]

        for id in sorted(ids):
            print(f' Task #{id} '.center(80, '-'))

            with open(f'query_{id}.sql', encoding='utf-8') as file:
                cursor.execute(file.read())
                pprint(cursor.fetchall())

        try:
            connection.commit()
        except Error as e:
            warning(e)

        cursor.close()


if __name__ == '__main__':
    main()
