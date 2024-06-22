import pandas as pd

results = pd.read_excel(
    r'D:\documents\NTT\Rao Togo\Borough High Street\Deliveroo\Orders\Deliveroo Daily Orders - 2018-01-11.xlsx',
    sheet_name=None)

print(results['Rao Deli'])
