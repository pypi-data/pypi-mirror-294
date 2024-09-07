import pandas as pd

# DataFrame global con las columnas básicas
df_global = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'column1': [1, 2, 3, 4, 5],
    'column2': [None, 2, 3, None, 5],
    'column3': ['a', 'b', 'c', 'd', 'e'],
    'unique_ids': [1, 2, 3, 4, 5],  
    'duplicated_ids': [1, 2, 2, 4, 5],
    'match_column1': [11, 12, 13, 14, 15],
    'match_column2': [15, 14, 13, 12, 11],
    'match_column_with_duplicates': [11, 11, 13, 13, 15]
})

