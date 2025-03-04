import boto3
import os
import pandas as pd
import numpy as np
from insert_values import insert_value

def import_xlsx(xlsx_path: str):
    df = pd.read_excel(xlsx_path)
    df = df.replace({np.nan: None})
    for _, row in df.iterrows():
        insert_value(event=dict(row), context=None)

    message = f"{xlsx_path} successfully imported to {os.environ['TABLE_NAME']}"
    return {"message": message}

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "dsci551_acroDB"
    xlsx_path = os.path.join("data", "MAG_code_of_points.xlsx")
    print(import_xlsx(xlsx_path=xlsx_path))