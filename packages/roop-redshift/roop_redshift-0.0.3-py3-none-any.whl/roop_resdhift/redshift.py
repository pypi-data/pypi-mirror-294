import os
import time

import pandas as pd
import pandas.io.sql as psql
import psycopg2 as pg
from iiris_vaultlib.vault import vault
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

class Redshift:
    def __init__(self) -> None:
        self.host = os.environ["REDSHIFT_HOST"]
        self.database = os.environ["REDSHIFT_DB"]
        self.schema = os.environ["REDSHIFT_SCHEMA"]
        self.port = os.environ["REDSHIFT_PORT"]
        self.sslmode = os.environ["REDSHIFT_SSL_MODE"]
        self.user, self.pwd = self.get_redshift_service_user()

    def get_redshift_service_user(self):
        try:
            start_time = int(time.time()*1000.0)
            if not is_conn_user_valid():
                v=vault()
                v.connect_with_role(os.environ["REDSHIFT_IAM_ROLE"])
                user=v.get_redshift_service_user(os.environ["REDSHIFT_ENV"], os.environ["REDSHIFT_DB_ROLE"])
                print("time taken to get redshift connection details from vault- %s ms", int(time.time()*1000.0) - start_time)
                return user['username'], user['password']
            else:
                redshift_user = os.environ("REDSHIFT_USER")
                print("return cached connction details redshift")
                return redshift_user['username'], redshift_user['password']
        except Exception as err:
            print(f" error - {err}")


    def get_client_session(self):
        return create_engine(
                f'redshift+psycopg2://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.database}?sslmode={self.sslmode}', poolclass=NullPool
                ).connect()


    def get_df(self, query: str, client_session=None):
        client = None
        if not client_session:
            client = self.get_client_session()
        else:
            client = client_session        
        _result: pd.DataFrame = psql.read_sql(text(query), client)
        if client is not None:
            client.close()
        return _result

def is_conn_user_valid():
    try:
        if os.environ("REDSHIFT_USER"):
            redshift_user = os.environ("REDSHIFT_USER")
            conn = pg.connect(
                            host=os.environ["REDSHIFT_HOST"],
                            database=os.environ["REDSHIFT_DB"],
                            port=os.environ["REDSHIFT_PORT"],
                            user=redshift_user['username'],
                            password=redshift_user['password']
                        )
            conn.close()
            return True
        else:
            return False
    except Exception as e:
        print(f"redshift user connection error - {e}")
        return False