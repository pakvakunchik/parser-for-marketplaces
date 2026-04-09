import os
import glob
import pandas as pd
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

def read_xls():
    try:
        raw_path = os.getenv('folder_path_xlss')
        folder_path = raw_path.strip() if raw_path else None
        if not folder_path:
            logger.warning(f'переменная "folder_path_xlss" не задана ')
            return None
        files = glob.glob(os.path.join(folder_path, '*.xlsx'))
        if not files:
            logger.warning(f'файлы в папке {folder_path} не найдены')
        dataframe = []
        for file in files:
            try:
                df = pd.read_excel(file)
                dataframe.append(df)
                logger.success(f'файл {os.path.basename(file)} прочитан')
                all_data = pd.concat(dataframe, ignore_index=True)
                return all_data
            except:
                logger.warning(f'file {os.path.basename(file)} is NOT read')
    except Exception as e:
        logger.warning(f'ошибка:{e}\nпапка {os.getenv()} пустая')

