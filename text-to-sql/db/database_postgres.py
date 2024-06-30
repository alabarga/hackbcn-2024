
import os,sys
import psycopg2
import pandas as pd
from database import DatabaseManager
import yaml
import os 



class DatabasePostgres(DatabaseManager):
    def __init__(self):
       pass

    def load_yaml_file(file_path: str):
        with open(file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        return data

    def get_credentials(self):
        return {'user': 'postgres', 'password': 'postgres', 'host': 'localhost', 'port': 5432, 'database': 'postgres'}
    #self.load_yaml_file(f'secrets/secret.yml')['postgres']
                
    def get_connection(self):
        credentials = self.get_credentials()
        return psycopg2.connect(**credentials)

    def execute_query(self, query:str)->int:
        conn = self.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    def select(self, query: str, params: dict = None) -> pd.DataFrame:
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            result = cur.fetchall()    
        return pd.DataFrame(result, columns=columns)
        

    def insert_many(self, schema:str,table_name:str, data:pd.DataFrame,column_names:str)->int:
       
        conn = self.get_connection()
        if data.empty:
            print("No data to insert.")
            return 0
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        values  = ', '.join(['%s'] * len(data[0]))
        query = f'INSERT INTO "{schema}"."{table_name}" ({column_names}) VALUES ({values})'
        with conn.cursor() as cur:
            cur.executemany(query, [tuple(row.values()) for row in data])
            conn.commit()
        return cur.rowcount

    def update(self, schema: str, table_name: str, data: pd.DataFrame, condition: str) -> int:

        conn = self.get_connection()
        if data.empty:
            print("No data to insert.")
            return 0
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        values = ', '.join([f"{key} = %s" for key in data[0]])
        query = f'UPDATE "{schema}"."{table_name}" SET {values} WHERE {condition}'
        with conn.cursor() as cur:
            for row in data:
                cur.execute(query, tuple(row.values()))
            conn.commit()
        return cur.rowcount
    
    def delete(self, schema: str, table_name: str, condition: str) -> int:
        conn = self.get_connection()
        query = f'DELETE FROM "{schema}"."{table_name}" WHERE {condition}'
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
        return cur.rowcount
    
    def execute_script(self, file_path: str) -> None:
        with open(file_path, 'r') as file:
            sql_script = file.read()
        self.execute_query(sql_script)


    def copy(self, filepath:str,table: str,schema:str,columns:list,delimeter:str=',') -> bool:
        conn = self.get_connection()
        columns = ','.join(columns)
        with conn.cursor() as cursor:
            copy_sql = f"""
                COPY {schema}.{table} ({columns}) FROM stdin WITH CSV HEADER
            DELIMITER E'\t';
                """
            with open(filepath, 'r') as file:
                cursor.copy_expert(sql=copy_sql, file=file)
                conn.commit()
        return True


if __name__=='__main__':
    print("DatabasePostgres class")
    db=DatabasePostgres()
    print(db.get_credentials())
    #db.execute_script('ddl/omop_cdm_schema.sql')
