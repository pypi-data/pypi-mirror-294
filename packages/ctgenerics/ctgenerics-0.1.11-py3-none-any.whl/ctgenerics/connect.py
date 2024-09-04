import os
import time
from pydantic import BaseModel, ValidationError
from typing import Optional, Any
import sqlalchemy
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd


class MissingConfigError(Exception):
    def __init__(self,message:str ='Configuration file not found. Please set the environment variable, CTGENERICS_CONFIG, or create a config.yaml file in the root directory. An example config file can be seen in ./config/sample_config.yaml'):
        self.message = message
        super().__init__(self.message)

class DBConfig(BaseModel):
    host: str
    port: int
    dbname: str
    user: str
    password: str
    default_schema: Optional[str] = None



def load_dbconfig(config_path:str,source:str, **kwargs: Any) -> DBConfig:
    try:
        with open(config_path,'r') as f:
            db_config = yaml.safe_load(f)
            if source in db_config:
                credentials = db_config[source]
                return DBConfig(**credentials)   
            else:
                raise ValueError(f'No credentials found for source: {source}')
    except FileNotFoundError:
        print(f"The configuration file {config_path} was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except ValidationError as e:
        print(f"Error validating configuration data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    raise MissingConfigError()




class Redshift:
    def __init__(self, source:str, schema: Optional[str] =None, config_path: Optional[str] = None):
        config_path = config_path or os.getenv('CTGENERICS_CONFIG')
        if not os.path.exists(config_path):
        # Fallback to default config file if main config_path is invalid
            if os.path.exists('config.yaml'):
                config_path = 'config.yaml'
            else:
                # Raise an error if no valid configuration is found
                raise MissingConfigError(f"Configuration file {config_path} not found.")
        db_config = load_dbconfig(config_path, source)
        self.db_config = db_config
    
        conn_str = f'postgresql://{self.db_config.user}:{self.db_config.password}@{self.db_config.host}:{self.db_config.port}/{self.db_config.dbname}'
        
        self.engine = create_engine(conn_str)
        self.conn = self.engine.connect()
        self.Session = sessionmaker(bind=self.engine)()


    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def download_table_to_df(self, table_name):
        tic = time.perf_counter()
        table_handle = sqlalchemy.Table(
            table_name,
            self.meta,
            autoload=True,
            autoload_with=self.conn,
            postgresql_ignore_search_path=True,
        )
        col_names = table_handle.columns.keys()

        query = sqlalchemy.select([table_handle])  # .limit(1000000)
        try:
            res_proxy = self.conn.execute(query)
            res_set = res_proxy.fetchall()
            res_proxy.close()
            df = pd.DataFrame(res_set, columns=col_names)
            toc = time.perf_counter()
            elapsed_time = toc - tic
            print("Connect.Redshift class took ", elapsed_time, " seconds to fetch all")
            return df
        except SQLAlchemyError as e:
            # error = str(e)
            return e

    def run_sql(self, sql_code, debug=True):
        try:
            tic = time.perf_counter()
            result = self.conn.execute(sqlalchemy.text(sql_code))
            toc = time.perf_counter()
            elapsed_time = toc - tic
            if debug:
                print(
                    "Connect.Redshift class took ",
                    "{0:.2f}".format(elapsed_time),
                    " seconds to run SQL code",
                )
            return result
        except SQLAlchemyError as e:
            return e

    def write_to_sql(
        self, df, tablename, schema="corpdev", index_label=None, if_exists="append"
    ):
        # make sure tablename is lowercase or it wont work if the table already exists.
        try:
            tic = time.perf_counter()
            df.to_sql(
                tablename,
                con=self.conn,
                if_exists=if_exists,
                schema=schema,
                index=False,
                index_label=index_label,
                chunksize=50000,
                method="multi",
            )
            toc = time.perf_counter()
            elapsed_time = toc - tic
            print(
                "Connect.Redshift class took ",
                "{0:.2f}".format(elapsed_time),
                " seconds to run SQL code",
            )
            # return result
        except SQLAlchemyError as e:
            print(e.__dict__["orig"])
            return e
        
def rs_run_sql(source:str, sql:str, debug:bool=True) -> None:
    ds = Redshift(source=source)
    ds.run_sql(sql, debug=debug)
    ds.conn.close()


def rs_run_sql_and_download_to_df(source:str, sql:str, debug:bool=True) -> pd.DataFrame:
    ds = Redshift(source=source)
    answers = ds.run_sql(sql, debug=debug)
    ret = answers.fetchall()
    keys = answers.keys()
    ds.conn.close()
    return pd.DataFrame(ret, columns=keys)