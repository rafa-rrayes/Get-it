import sqlite3
import inspect
class Database:
    def __init__(self, banco_de_dados):
        self.conn = sqlite3.connect(banco_de_dados+ '.db')
        self.cur = self.conn.cursor()
        self.tables = {}
        self.table = None

    def new_table(self, table):
        text= str(inspect.signature(table.__init__))
        name = table.__name__
        text = text[7:-9]
        text = text.split(',')
        keys = [k.split(':')[0].strip() for k in text]
        types = [t.split('=')[1].strip()[1:-1] for t in text]
        structure = "id integer primary key autoincrement,\n"
        for key, type in zip(keys, types):
            structure += key +' '+ type + ',\n'
        structure = structure[:-2]
        print(structure)
        self.tables[name] = {"structure":structure, "keys":keys, "types":types}
        self.command(f"""CREATE TABLE IF NOT EXISTS {name} ( {structure} );""")
    def use(self, table):
        if type(table) == str:
            name = table
        elif type(table) == type:
            name = table.__name__
        
        if name not in self.tables:
            cursor = self.conn.cursor()
            # Get the SQL statement used to create the table
            table_name = name  # Replace with your actual table name
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            # Fetch the creation SQL statement
            fetch = cursor.fetchone()
            if fetch == None:
                raise Exception(f"There is no table named `{table_name}`. Make sure you create the table before using it.")
            text = fetch[0]
            structure = text.split('(')[1][1:-2]
            keys = structure.replace(',', '').split('\n')
            types = [' '.join(k.split(' ')[1:]) for k in keys]
            keys = [k.split(' ')[0] for k in keys]
            self.tables[name] = {"structure":structure, "keys":keys, "types":types}
        self.table = name
        self.keys_now = self.tables[self.table]["keys"]
    def command(self, comando):
        self.cur.execute(comando)
    def commit(self):
        self.conn.commit()
    def add(self, row):
        if self.table == None:
            raise Exception("No table is being used at the moment.\nUse Database.use() to select a table to add")
        values = ''
        for key in self.keys_now:
            values += "'"+ str(getattr(row,key)) +  "'" + " , " 
        values = values[:-3]
        comando = f"INSERT INTO {self.table} ({' , '.join(self.keys_now)}) VALUES ({values});"
        self.command(comando)
    def get_all(self):
        if self.table == None:
            raise Exception("No table is being used at the moment.\nUse Database.use() to select a table to get all")
        cursor = self.conn.execute(f"SELECT {' , '.join(self.keys_now)} FROM {self.table}")
        rows = []
        for line in cursor:
            dic = {}
            for key, value in zip(self.keys_now, line):
                dic[key] = value
            rows.append(dic)
        return rows
    def update(self, row, selector):
        if self.table == None:
            raise Exception("No table is being used at the moment.\nUse Database.use() to select a table to update")
        atual = str(getattr(row, selector))
        values = ''
        for key in self.keys_now:
            values += "'"+ str(getattr(row,key)) +  "'" + "," 
        values = values[:-1].split(',')
        text = ""
        for key, value in zip(self.keys_now, values):
            text += key + ' = ' + value + ' , '
        text = text[:-3]
        comando = f"UPDATE {self.table} SET {text} WHERE {selector} = {atual}"
        self.command(comando)
    def delete(self, key, value):
        if self.table == None:
            raise Exception("No table is being used at the moment.\nUse Database.use() to select a table to delete from")
        self.command(f"DELETE FROM {self.table} WHERE {key} = '{value}'")