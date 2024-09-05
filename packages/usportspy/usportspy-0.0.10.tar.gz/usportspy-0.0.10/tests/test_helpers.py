
def print_columns(df):
    columns = df.columns.tolist()
    if len(columns) > 1:
        columns_str = ", ".join(columns[:-1]) + ", and " + columns[-1]
    else:
        columns_str = columns[0]
    
    print(f"columns: {columns_str}\n")


