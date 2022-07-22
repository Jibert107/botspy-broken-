import sqlite3


class DB:
    _instance = None

    # SINGLETON : chaque DB() ramenera le même objet et on évitera les ouvertures multiples du même fichier SQLITE
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self) -> None:
        self.__sqlite3 = sqlite3.connect("database.sqlite")
        pass

    def insert(self, table: str, fields: iter, values):
        sql_fields = ",".join(fields)
        valuesTemplates = ",".join(list(map(lambda x: "?", fields)))
        query = f"INSERT INTO {table} ({sql_fields}) VALUES({valuesTemplates})"
        self.__sqlite3.execute(query, values)
        self.__sqlite3.commit()

    def select(self, table, fields='*', orderby=['message_date', 'DESC'], limit=10):
        if isinstance(fields, list):
            if(len(fields) > 1):
                fields = ",".join(fields)
            else:
                fields = fields[0]
        orderby = " ".join(orderby)
        query = f"SELECT {fields} FROM {table} ORDER BY {orderby} LIMIT {limit}"
        result = self.__sqlite3.execute(query)
        return result.fetchall()
