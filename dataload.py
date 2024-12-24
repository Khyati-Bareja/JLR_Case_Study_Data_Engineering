#Loading Layer : 

import sqlite3
import pandas as pd

def load_data_to_sql(df, db_name='production.db', table_name='production_cost_table'):
    conn = sqlite3.connect(db_name)

    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()    