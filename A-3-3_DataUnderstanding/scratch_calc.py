import pandas as pd
import numpy as np

print("Loading data...")
df = pd.read_csv('Data/online_retail_II.csv')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Is_C'] = df['Invoice'].astype(str).str.startswith('C')
df['LineTotal'] = df['Quantity'] * df['Price']

print(f"Total rows: {len(df):,}")
c_rows = df[df['Is_C']].copy()
print(f"Total C lines: {len(c_rows):,}")
print(f"C lines with Customer ID: {c_rows['Customer ID'].notnull().sum():,} ({c_rows['Customer ID'].notnull().mean()*100:.2f}%)")
print(f"C lines without Customer ID: {c_rows['Customer ID'].isnull().sum():,} ({c_rows['Customer ID'].isnull().mean()*100:.2f}%)")

# Inspect C lines without Customer ID
c_no_cust = c_rows[c_rows['Customer ID'].isnull()]
print(f"Distinct Invoices in C without Customer ID: {c_no_cust['Invoice'].nunique():,}")
print(f"Price distribution of C without Customer ID: min={c_no_cust['Price'].min()}, median={c_no_cust['Price'].median()}, max={c_no_cust['Price'].max()}")
print("Sample descriptions of C without Customer ID:")
print(c_no_cust['Description'].value_counts().head(10))

# In c_rows with Customer ID:
cust_c = c_rows[c_rows['Customer ID'].notnull()].copy()
cust_pos = df[df['Customer ID'].notnull() & ~df['Is_C'] & (df['Quantity'] > 0)].copy()

cust_c_pairs = set(zip(cust_c['Customer ID'], cust_c['StockCode']))
cust_pos_pairs = set(zip(cust_pos['Customer ID'], cust_pos['StockCode']))

matched_pairs = cust_c_pairs.intersection(cust_pos_pairs)
orphan_pairs = cust_c_pairs - cust_pos_pairs

print(f"\nDistinct Customer-SKU cancellation pairs: {len(cust_c_pairs):,}")
print(f"Pairs with matching positive purchase: {len(matched_pairs):,} ({len(matched_pairs)/len(cust_c_pairs)*100:.2f}%)")
print(f"Orphan cancellation pairs (NO purchase record in window): {len(orphan_pairs):,} ({len(orphan_pairs)/len(cust_c_pairs)*100:.2f}%)")

cust_c['is_orphan'] = cust_c.apply(lambda r: (r['Customer ID'], r['StockCode']) in orphan_pairs, axis=1)
print(f"C lines that are orphan: {cust_c['is_orphan'].sum():,} ({cust_c['is_orphan'].mean()*100:.2f}%)")
print(f"C lines that have matching purchases: {(~cust_c['is_orphan']).sum():,} ({(~cust_c['is_orphan']).mean()*100:.2f}%)")

# Now let's analyze the matched pairs:
# For matched pairs, how many times does the cancellation happen:
# A) AFTER the positive purchase (standard return / post-purchase cancellation)
# B) BEFORE the positive purchase (re-bill / corrected re-entry where true order comes AFTER)
# C) Both (customer has multiple positive and negative transactions)

# Merge matched records
cust_matched_c = cust_c[~cust_c['is_orphan']]
merged = pd.merge(
    cust_matched_c[['Invoice', 'StockCode', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID']],
    cust_pos[['Invoice', 'StockCode', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID']],
    on=['Customer ID', 'StockCode'],
    suffixes=('_c', '_pos')
)
merged['days_diff'] = (merged['InvoiceDate_pos'] - merged['InvoiceDate_c']).dt.total_seconds() / 86400.0

print("\n--- TEMPORAL TIMING OF CANCELLATIONS VS POSITIVE PURCHASES ---")
# Let's inspect unique C lines:
# Group by (Invoice_c, StockCode):
grouped_c = merged.groupby(['Invoice_c', 'StockCode'])
pure_post_return = 0
has_rebill_after = 0 # pos date > c date
immediate_correction = 0 # pos date > c date and within 24h

for (inv, sc), grp in grouped_c:
    pos_dates = grp['InvoiceDate_pos']
    c_date = grp['InvoiceDate_c'].iloc[0]
    
    # Are there positive purchases after the cancellation?
    after = grp[grp['days_diff'] > 0]
    before = grp[grp['days_diff'] <= 0]
    
    if len(after) > 0 and len(before) == 0:
        # Only pos after cancellation! The true sale came AFTER the cancellation!
        has_rebill_after += 1
        if (after['days_diff'] <= 1.0).any():
            immediate_correction += 1
    elif len(before) > 0 and len(after) == 0:
        pure_post_return += 1
    else:
        # Has purchases both before and after
        has_rebill_after += 1
        if (after['days_diff'] <= 1.0).any():
            immediate_correction += 1

total_c_lines_matched = grouped_c.ngroups
print(f"Total matched C line items: {total_c_lines_matched:,}")
print(f"Pure post-purchase returns (bought first, cancelled later): {pure_post_return:,} ({pure_post_return/total_c_lines_matched*100:.2f}%)")
print(f"Cancellations followed by positive re-bill/purchase ('salía la verdadera después'): {has_rebill_after:,} ({has_rebill_after/total_c_lines_matched*100:.2f}%)")
print(f"  Of which immediate system correction/re-bill within 24h: {immediate_correction:,} ({immediate_correction/total_c_lines_matched*100:.2f}%)")

# Multiple cancellations for the same item:
mult_c = cust_c.groupby(['Customer ID', 'StockCode']).size()
print(f"\nCustomer-SKU pairs with exactly 1 cancellation: {(mult_c == 1).sum():,} ({(mult_c == 1).mean()*100:.2f}%)")
print(f"Customer-SKU pairs with MULTIPLE cancellations (>=2): {(mult_c >= 2).sum():,} ({(mult_c >= 2).mean()*100:.2f}%)")
print(f"Customer-SKU pairs with >= 5 cancellations: {(mult_c >= 5).sum():,}")
print(f"Max cancellations for a single Customer-SKU pair: {mult_c.max():,}")
