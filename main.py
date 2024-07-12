from logging import WARNING, basicConfig, warning
from random import randint
from sqlite3 import Cursor, Error, connect

TABLES = {
    'groups': {
        'rows': 3
    },
    'students': {
        'relations': ('groups',),
        'rows': randint(30, 50)
    },
    'teachers': {
        'rows': randint(3, 5)
    },
    'subjects': {
        'relations': ('teachers',),
        'rows': randint(5, 8)
    },
    'grades': {
        'relations': ('students', 'subjects'),
        'column': 'value',
        'type': 'TINYINT UNSIGNED',
        'rows': randint(0, 20)
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

    cursor.executemany(
        query,
        [(f'{name.title()}  #{id + 1}',
          *[randint(1, TABLES[relation]['rows']) for relation in relations])
         for id in range(TABLES[name]['rows'])]
    )


def main() -> None:
    basicConfig(level=WARNING)

    with connect('db.sqlite') as connection:
        cursor = connection.cursor()

        [table(cursor, name) for name in TABLES.keys()]

        try:
            connection.commit()
        except Error as e:
            warning(e)

        cursor.close()


if __name__ == '__main__':
    main()
