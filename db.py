import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS employees(
            id Integer Primary Key,
            name text,
            alias text,
            startDate text,
            jobTitle text,
            email text,
            suite text,
            mirror text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    # Insert Function
    def insert(self, name, alias, startDate, jobTitle, email, suite, mirror):
        self.cur.execute("insert into employees(name, alias, startDate, jobTitle, email, suite, mirror) values (?,?,?,?,?,?,?)",
                         (name, alias, startDate, jobTitle, email, suite, mirror))
        self.con.commit()

    # Fetch All Data from DB
    def fetch(self):
        self.cur.execute("SELECT * from employees")
        rows = self.cur.fetchall()
        # print(rows)
        return rows

    # Delete a Record in DB
    def remove(self, id):
        self.cur.execute("delete from employees where id=?", (id,))
        self.con.commit()

    # Update a Record in DB
    def update(self, id,  name, alias, startDate, jobTitle, email, suite, mirror):
        self.cur.execute(
            "update employees set name=?, alias=?, startDate=?, jobTitle=?, email=?, suite=?, mirror=? where id=?",
            (alias, name, startDate, jobTitle, email, suite, mirror,id))
        self.con.commit()
