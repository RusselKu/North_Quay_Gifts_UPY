import pandas as pd
import numpy as np
import scipy.stats as stats
import json

print("Loading dataset...")
df = pd.read_csv("Data/online_retail_II.csv")

total_rows = len(df)
total_cols = df.shape[1]

# Convert InvoiceDate
df['InvoiceDateParsed'] = pd.to_datetime(df['InvoiceDate'])
min_date = df['InvoiceDateParsed'].min()
max_date = df['InvoiceDateParsed'].max()

distinct_invoices = df['Invoice'].nunique()
distinct_customers = df['Customer ID'].dropna().nunique()

print(f"Total Rows: {total_rows}")
print(f"Total Columns: {total_cols}")
print(f"Min Date: {min_date}")
print(f"Max Date: {max_date}")
print(f"Distinct Invoices: {distinct_invoices}")
print(f"Distinct Customers (Identified): {distinct_customers}")

# Multi-product invoice example
inv_counts = df.groupby('Invoice').agg(
    total_lines=('StockCode', 'count'),
    distinct_stockcodes=('StockCode', 'nunique')
)
multi_item_diff = inv_counts[inv_counts['total_lines'] > inv_counts['distinct_stockcodes']].head(5)
print("\nMulti-item invoices with duplicate stockcodes:")
print(multi_item_diff)

sample_inv = "489434"
print(f"\nSample Invoice {sample_inv}:")
sample_data = df[df['Invoice'] == sample_inv]
print(f"Lines: {len(sample_data)}, Unique StockCodes: {sample_data['StockCode'].nunique()}")

# First and last month coverage
df['YearMonth'] = df['InvoiceDateParsed'].dt.to_period('M')
ym_counts = df.groupby('YearMonth').agg(
    lines=('Invoice', 'count'),
    first_day=('InvoiceDateParsed', lambda x: x.min().strftime('%Y-%m-%d %H:%M')),
    last_day=('InvoiceDateParsed', lambda x: x.max().strftime('%Y-%m-%d %H:%M')),
    days_present=('InvoiceDateParsed', lambda x: x.dt.day.nunique())
)
print("\nYearMonth coverage:")
print(ym_counts.iloc[[0, 1, -2, -1]])

# Section 2: Descriptive Statistics
q_s = df['Quantity']
p_s = df['Price']

desc_stats = {
    'Quantity': {
        'count': int(q_s.count()),
        'mean': float(q_s.mean()),
        'median': float(q_s.median()),
        'std': float(q_s.std()),
        'min': float(q_s.min()),
        'q1': float(q_s.quantile(0.25)),
        'q3': float(q_s.quantile(0.75)),
        'max': float(q_s.max()),
        'skew': float(q_s.skew()),
        'kurt': float(q_s.kurt()) # Fisher's excess kurtosis (default in pandas)
    },
    'Price': {
        'count': int(p_s.count()),
        'mean': float(p_s.mean()),
        'median': float(p_s.median()),
        'std': float(p_s.std()),
        'min': float(p_s.min()),
        'q1': float(p_s.quantile(0.25)),
        'q3': float(p_s.quantile(0.75)),
        'max': float(p_s.max()),
        'skew': float(p_s.skew()),
        'kurt': float(p_s.kurt())
    }
}
print("\nDescriptive statistics:")
print(pd.DataFrame(desc_stats))

# Categorical summary: Country and StockCode
cat_stats = {
    'Country': {
        'count': int(df['Country'].count()),
        'nunique': int(df['Country'].nunique()),
        'top': str(df['Country'].mode()[0]),
        'top_freq': int(df['Country'].value_counts().iloc[0]),
        'nulls': int(df['Country'].isna().sum())
    },
    'StockCode': {
        'count': int(df['StockCode'].count()),
        'nunique': int(df['StockCode'].nunique()),
        'top': str(df['StockCode'].mode()[0]),
        'top_freq': int(df['StockCode'].value_counts().iloc[0]),
        'nulls': int(df['StockCode'].isna().sum())
    }
}
print("\nCategorical summary:")
print(pd.DataFrame(cat_stats))

# Section 3: Univariate Analysis
top3_country = df['Country'].value_counts().head(3)
top3_stockcode = df['StockCode'].value_counts().head(3)

print("\nTop 3 Countries:")
for cat, count in top3_country.items():
    print(f"{cat}: {count} lines ({count / total_rows * 100:.2f}%)")

print("\nTop 3 StockCodes:")
for cat, count in top3_stockcode.items():
    print(f"{cat}: {count} lines ({count / total_rows * 100:.2f}%)")

top10_country = df['Country'].value_counts().head(10)
top10_stock = df['StockCode'].value_counts().head(10)
print(f"Top 10 Countries coverage: {top10_country.sum()} lines ({top10_country.sum()/total_rows*100:.2f}%)")
print(f"Top 10 StockCodes coverage: {top10_stock.sum()} lines ({top10_stock.sum()/total_rows*100:.2f}%)")

# Section 4: Data Quality Diagnostics
nulls_df = pd.DataFrame({
    'Nulls': df.isna().sum(),
    'Percent': df.isna().sum() / total_rows * 100
})
print("\nNull values:")
print(nulls_df)

dups = df.duplicated().sum()
q_neg = (df['Quantity'] < 0).sum()
q_zero = (df['Quantity'] == 0).sum()
p_neg = (df['Price'] < 0).sum()
p_zero = (df['Price'] == 0).sum()

situations = pd.DataFrame({
    'Situation': ['Duplicados exactos adicionales', 'Quantity < 0', 'Quantity = 0', 'Price < 0', 'Price = 0'],
    'Lines': [dups, q_neg, q_zero, p_neg, p_zero],
    'Percent': [dups/total_rows*100, q_neg/total_rows*100, q_zero/total_rows*100, p_neg/total_rows*100, p_zero/total_rows*100]
})
print("\nSituations:")
print(situations)

# Section 5: Cancellations and Negatives
is_c = df['Invoice'].astype(str).str.startswith('C')
c_lines = is_c.sum()
c_invs = df[is_c]['Invoice'].nunique()
c_q_neg = (is_c & (df['Quantity'] < 0)).sum()
c_q_zero = (is_c & (df['Quantity'] == 0)).sum()
c_q_pos = (is_c & (df['Quantity'] > 0)).sum()

print("\nCancellations (C prefix):")
print(f"Lines with C: {c_lines}")
print(f"Distinct C Invoices: {c_invs}")
print(f"C with Quantity < 0: {c_q_neg}")
print(f"C with Quantity = 0: {c_q_zero}")
print(f"C with Quantity > 0: {c_q_pos}")

# Negative quantities without C
no_c_q_neg = (~is_c & (df['Quantity'] < 0))
no_c_lines = no_c_q_neg.sum()
no_c_invs = df[no_c_q_neg]['Invoice'].nunique()
print(f"\nNegative Quantities without C:")
print(f"Lines: {no_c_lines}")
print(f"Distinct Invoices: {no_c_invs}")

# Contingency table
ctab = pd.crosstab(is_c.map({True: 'Con C', False: 'Sin C'}), 
                   pd.cut(df['Quantity'], bins=[-np.inf, -0.0001, 0.0001, np.inf], labels=['Quantity < 0', 'Quantity = 0', 'Quantity > 0']),
                   margins=True)
print("\nContingency Table:")
print(ctab)

# Inspect negative without C cases
sample_no_c = df[no_c_q_neg].head(10)
print("\nSample Negative without C:")
print(sample_no_c[['Invoice', 'StockCode', 'Description', 'Quantity', 'Price', 'Customer ID', 'InvoiceDate']])

# Check Price < 0 cases
p_neg_cases = df[df['Price'] < 0]
print("\nNegative Price cases:")
print(p_neg_cases[['Invoice', 'StockCode', 'Description', 'Quantity', 'Price', 'Customer ID']])

# Check Price == 0 cases
p_zero_cases = df[df['Price'] == 0]
print(f"\nPrice == 0 cases: {len(p_zero_cases)}")
print("Price == 0 with Customer ID:", p_zero_cases['Customer ID'].notna().sum())
print("Price == 0 without Customer ID:", p_zero_cases['Customer ID'].isna().sum())
print("Top descriptions for Price == 0:")
print(p_zero_cases['Description'].value_counts().head(10))

# Save all exact calculations to JSON for reference
output_dict = {
    'total_rows': total_rows,
    'total_cols': total_cols,
    'min_date': str(min_date),
    'max_date': str(max_date),
    'distinct_invoices': distinct_invoices,
    'distinct_customers': distinct_customers,
    'desc_stats': desc_stats,
    'cat_stats': cat_stats,
    'top3_country': {k: {'lines': int(v), 'pct': float(v/total_rows*100)} for k, v in top3_country.items()},
    'top3_stockcode': {k: {'lines': int(v), 'pct': float(v/total_rows*100)} for k, v in top3_stockcode.items()},
    'situations': situations.to_dict(orient='records'),
    'c_lines': int(c_lines),
    'c_invs': int(c_invs),
    'c_q_neg': int(c_q_neg),
    'c_q_zero': int(c_q_zero),
    'c_q_pos': int(c_q_pos),
    'no_c_q_neg_lines': int(no_c_lines),
    'no_c_q_neg_invs': int(no_c_invs)
}

with open("A-3-3_DataUnderstanding/computed_stats.json", "w") as f:
    json.dump(output_dict, f, indent=4)
print("\nSaved computed_stats.json successfully!")
