import os
import time
import pandas.io.sql as psql
import psycopg2 as pg
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

class Postgres:

    def __init__(self, schema_name:str=None, operation:str="r") -> None:
        self.r_host = os.environ["PG_HOST_R"]
        self.w_host = os.environ["PG_HOST_W"]
        self.database = os.environ["PG_DB"]
        self.schema = schema_name
        self.port = int(os.environ["PG_PORT"])
        self.user, self.pwd = get_postgres_service_user()
        self.operation = operation
        self.read_connection = None
        self.write_connection = None
        self.pgengine_con = None
        
    def __enter__(self):
        print("PG - __enter__ - enter - operation %s", self.operation)
        if self.operation in ["r"]:
            self.read_connection = pg.connect(
                    host=self.r_host,
                    database=self.database,
                    port=self.port,
                    user=self.user,
                    password=self.pwd
                )
        if self.operation in ["e"]:
            self.read_connection = pg.connect(
                    host=self.w_host,
                    database=self.database,
                    port=self.port,
                    user=self.user,
                    password=self.pwd
                )
        if self.operation in ["w"]:
            # conn.close() will not close the connection if engine is connection pooled, it will return the connection to pool.
            # To close the connection disable the connection pooling using poolclass=NullPool
            self.write_connection = create_engine(
                f"postgresql://{self.user}:{self.pwd}@{self.w_host}:{self.port}/{self.database}", poolclass=NullPool
                ).connect()
        if self.operation in ["engine_rw"]:
            # conn.close() will not close the connection if engine is connection pooled, it will return the connection to pool.
            # To close the connection disable the connection pooling using poolclass=NullPool
            # new engine creation for DataFrame processing
            self.pgengine_con = create_engine(
                f"postgresql://{self.user}:{self.pwd}@{self.w_host}:{self.port}/{self.database}", poolclass=NullPool
                ).connect()
        if self.operation in ["engine_rw"]:
            self.pgengine_con = create_engine(
                f"postgresql://{self.user}:{self.pwd}@{self.w_host}:{self.port}/{self.database}", poolclass=NullPool
                ).connect()
        print("PG - __enter__ - exit - operation %s", self.operation)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("PG - __enter__ - enter")
        if self.operation in ["r","rw"]:
            self.read_connection.close()
        if self.operation in ["w","rw"]:
            # self.write_connection.commit()
            self.write_connection.close()
        if self.operation in ['engine_rw']:
            self.pgengine_con.close()
        print("PG - __enter__ - exit")

    def read(self, sql, params=None):
        con = self.pgengine_con if self.pgengine_con else self.read_connection
        df = psql.read_sql(sql, con, params=params)
        return df

    def execute_update(self, sql):
        print("PG - execute_update - exit - %s", sql)        
        self.write_connection.execute(sql)
        self.write_connection.close()
        print("PG - execute_update - exit - %s", sql)
        
    def execute(self, sql):
        print("PG - execute - exit - %s", sql)        
        cursor = self.read_connection.cursor()
        cursor.execute(sql)
        self.read_connection.commit()
        cursor.close()
        print("PG - execute - exit - %s", sql)
        
    def execute_many(self, sql_list):
        cursor = self.read_connection.cursor()
        num_rows_affected = []
        for sql in sql_list:
            cursor.execute(sql)
            num_rows_affected.append(cursor.rowcount)
        self.read_connection.commit()
        cursor.close()
        return len(num_rows_affected)
    
    def insert(self, df, table, if_exists="append"):
        return df.to_sql(
            name=table, 
            con=self.pgengine_con if self.pgengine_con else self.write_connection, 
            if_exists=if_exists, 
            index=False, 
            schema=self.schema
        )

    def update(self, df, table, if_exists="append", ignore_contraint=False):
        method_type = postgres_upsert
        if ignore_contraint:
            method_type = postgres_upsert_ignore_constraint
        return df.to_sql(
            name=table,
            con=self.write_connection,
            if_exists=if_exists,
            index=False,
            schema=self.schema,
            method=method_type
        )

def postgres_upsert(table, conn, keys, data_iter):

    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_update(
        constraint=f"{table.table.name}_pkey",
        set_={c.key: c for c in insert_statement.excluded},
    )
    res = conn.execute(upsert_statement)
    return res.rowcount

def postgres_upsert_ignore_constraint(table, conn, keys, data_iter):
    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]
    insert_statement = insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_nothing()
    res = conn.execute(upsert_statement)
    return res.rowcount

def is_conn_user_valid():
    try:
        if os.getenv("PG_USER"):
            pg_user = os.getenv("PG_USER")
            conn = pg.connect(
                            host=os.environ["PG_HOST_W"],
                            database=os.environ["PG_DB"],
                            port=os.environ["PG_PORT"],
                            user=pg_user['username'],
                            password=pg_user['password']
                        )
            conn.close()
            return True
        else:
            return False
    except Exception as e:
        print(f"postgres user connection error - {e}")
        return False

def get_postgres_service_user():
    try:
        start_time = int(time.time()*1000.0)
        if not is_conn_user_valid():
            # v=vault()
            # v.connect_with_role(os.environ["PG_IAM_ROLE"])
            # user=v.get_postgres_service_user(os.environ["PG_ENV"],os.environ["PG_DB_ROLE"])
            user=get_postgres_service_user(os.environ["PG_ENV"],os.environ["PG_DB_ROLE"])
            print("time taken to get postgres connection details from vault- %s ms", int(time.time()*1000.0) - start_time)
            return user['username'], user['password']
        else:
            pg_user = os.environ('PG_USER')
            print("returning cached connction details for postgres")
            return pg_user['username'], pg_user['password']
    except Exception as err:
        print(f"error - {err}")