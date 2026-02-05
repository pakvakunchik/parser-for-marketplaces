import sqlite3
import glob
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()


Base = declarative_base()
engine = create_engine('sqlite:///products.db')

def read_xls():
    folder_path = os.getenv('folder_path_xlss').strip()
    files = glob.glob(os.path.join(folder_path, '*.xlsx'))
    dataframe = []
    for file in files:
        try:
            df = pd.read_excel(file)
            dataframe.append(df)
            print(f'file {os.path.basename(file)} is read')
        except:
            print(f'file {os.path.basename(file)} is NOT read')
        all_data = pd.concat(dataframe)
    return all_data


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name_of_product = Column(String)
    description_of_product = Column(String)
    quantity = Column(Integer)
    barcode = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def db_write():
    engine = create_engine('sqlite:///products.db')
    df_to_save = read_xls()
    df_to_save.columns = [str(col).strip().lower() for col in df_to_save.columns]
    if 'id' in df_to_save.columns and 'quantity' in df_to_save.columns:
        df_to_save['id'] = pd.to_numeric(df_to_save['id'], errors='coerce')
        df_to_save['quantity'] = pd.to_numeric(df_to_save['quantity'], errors='coerce')
        df_to_save = df_to_save.dropna(subset=['id', 'quantity'])
        df_to_save = df_to_save['id'].astype(int)
        df_to_save['quantity'] = df_to_save['quantity'].astype(int)
        df_to_save = df_to_save[['id', 'quantity']]
        df_to_save.to_sql('products', engine, index=False, if_exists='append')
        print('save in db success')
    else:
        print('save in db failed')

db_write()

#
# cursor = conn.cursor()
# conn = sqlite3.connect('goods.db')
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS products
#                 (id INTEGER PRIMARY KEY,
#                 barcode TEXT UNIQUE)''')
# conn.commit()
# conn.close()
#
# while True:
#     barcode = input("введите штрихкод (или 'q' для выхода) : ")
#     if barcode == 'q':
#         break
#     else:
#         cursor.execute('''CREATE TABLE IF NOT EXISTS products
#                           (id INTEGER PRIMARY KEY,
#                            barcode TEXT UNIQUE)''')
#         conn.commit()
#         conn.close()
#         continue




















