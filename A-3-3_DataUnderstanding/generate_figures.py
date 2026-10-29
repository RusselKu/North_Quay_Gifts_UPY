import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica', 'Arial', 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

print("Loading data for figure generation...")
df = pd.read_csv("Data/online_retail_II.csv")
total_rows = len(df)

out_dir = "A-3-3_DataUnderstanding/figures"

# -------------------------------------------------------------
# FIG 1: Quantity Histogram (Full Range + Zoomed)
# -------------------------------------------------------------
print("Generating Figure 1: Quantity Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

# Full Range
ax1.hist(df['Quantity'], bins=100, color='#1f77b4', edgecolor='black', alpha=0.85)
ax1.set_yscale('log')
ax1.set_title("Full Range Quantity Distribution (Log Scale)", fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel("Quantity (Units)", fontsize=10)
ax1.set_ylabel("Frequency / Line Count (Log Scale)", fontsize=10)
ax1.axvline(0, color='red', linestyle='--', linewidth=1, label='Zero Quantity')
ax1.legend(loc='upper right', frameon=True)
ax1.grid(True, linestyle=':', alpha=0.6)

# Zoomed View [-50, 100]
q_zoom_mask = (df['Quantity'] >= -50) & (df['Quantity'] <= 100)
q_zoom = df.loc[q_zoom_mask, 'Quantity']
outside_pct = (1.0 - len(q_zoom) / total_rows) * 100

ax2.hist(q_zoom, bins=75, color='#2ca02c', edgecolor='black', alpha=0.85)
ax2.set_title("Zoomed View: [-50, 100] Units", fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel("Quantity (Units)", fontsize=10)
ax2.set_ylabel("Frequency / Line Count", fontsize=10)
ax2.axvline(0, color='red', linestyle='--', linewidth=1, label='Zero Quantity')
ax2.axvline(df['Quantity'].median(), color='darkblue', linestyle='-', linewidth=1.5, label=f'Median: {df["Quantity"].median():.0f}')
ax2.axvline(df['Quantity'].mean(), color='darkorange', linestyle=':', linewidth=1.5, label=f'Mean: {df["Quantity"].mean():.2f}')
ax2.text(0.04, 0.78, f"Coverage: {100-outside_pct:.2f}%\nOutside window: {outside_pct:.2f}%\nTotal Lines: {total_rows:,}", 
         transform=ax2.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", alpha=0.9))
ax2.legend(loc='upper right', frameon=True)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.suptitle("Figure 1. Empirical Distribution of Transaction Quantity (North Quay Gifts)", fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
fig.savefig(f"{out_dir}/fig1_quantity_hist.png", dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# FIG 2: Price Histogram (Full Range + Zoomed)
# -------------------------------------------------------------
print("Generating Figure 2: Price Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

# Full Range
ax1.hist(df['Price'], bins=100, color='#9467bd', edgecolor='black', alpha=0.85)
ax1.set_yscale('log')
ax1.set_title("Full Range Unit Price Distribution (Log Scale)", fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel("Price (GBP / Unit)", fontsize=10)
ax1.set_ylabel("Frequency / Line Count (Log Scale)", fontsize=10)
ax1.axvline(0, color='red', linestyle='--', linewidth=1, label='Zero Price')
ax1.legend(loc='upper right', frameon=True)
ax1.grid(True, linestyle=':', alpha=0.6)

# Zoomed View [0, 25]
p_zoom_mask = (df['Price'] >= 0) & (df['Price'] <= 25)
p_zoom = df.loc[p_zoom_mask, 'Price']
p_outside_pct = (1.0 - len(p_zoom) / total_rows) * 100

ax2.hist(p_zoom, bins=50, color='#8c564b', edgecolor='black', alpha=0.85)
ax2.set_title("Zoomed View: [£0.00, £25.00] GBP", fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel("Price (GBP / Unit)", fontsize=10)
ax2.set_ylabel("Frequency / Line Count", fontsize=10)
ax2.axvline(df['Price'].median(), color='darkblue', linestyle='-', linewidth=1.5, label=f'Median: £{df["Price"].median():.2f}')
ax2.axvline(df['Price'].mean(), color='darkorange', linestyle=':', linewidth=1.5, label=f'Mean: £{df["Price"].mean():.2f}')
ax2.text(0.55, 0.78, f"Coverage: {100-p_outside_pct:.2f}%\nOutside window: {p_outside_pct:.2f}%\nTotal Lines: {total_rows:,}", 
         transform=ax2.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", alpha=0.9))
ax2.legend(loc='upper right', frameon=True)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.suptitle("Figure 2. Empirical Distribution of Unit Price in GBP (North Quay Gifts)", fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
fig.savefig(f"{out_dir}/fig2_price_hist.png", dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# FIG 3: Country Frequencies (Top 10)
# -------------------------------------------------------------
print("Generating Figure 3: Country Frequencies...")
top10_c = df['Country'].value_counts().head(10)
top10_c_pct = (top10_c / total_rows) * 100

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
bars = ax.barh(top10_c.index[::-1], top10_c.values[::-1], color='#1f77b4', edgecolor='black', alpha=0.85)
ax.set_title("Figure 3. Top 10 Countries by Transaction Line Frequency", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Line Count (Number of Records)", fontsize=10)
ax.set_ylabel("Country", fontsize=10)
ax.set_xscale('log') # Log scale helps show non-UK countries clearly
ax.grid(True, linestyle=':', alpha=0.6, which='both')

for bar, count, pct in zip(bars, top10_c.values[::-1], top10_c_pct.values[::-1]):
    ax.text(count * 1.15, bar.get_y() + bar.get_height()/2, f"{count:,} ({pct:.2f}%)", 
            va='center', ha='left', fontsize=8.5, fontweight='bold', color='#222222')

ax.text(0.03, 0.12, f"Total Countries: {df['Country'].nunique()}\nTop 10 Total: {top10_c.sum():,} lines ({top10_c.sum()/total_rows*100:.2f}%)\nUK Share: {top10_c.iloc[0]/total_rows*100:.2f}%", 
        transform=ax.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="#f8f9fa", ec="#cccccc", alpha=0.95))

plt.tight_layout()
fig.savefig(f"{out_dir}/fig3_country_bar.png", dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# FIG 4: StockCode Frequencies (Top 10)
# -------------------------------------------------------------
print("Generating Figure 4: StockCode Frequencies...")
top10_s = df['StockCode'].value_counts().head(10)
top10_s_pct = (top10_s / total_rows) * 100

# Get representative description for top stockcodes
desc_map = {}
for sc in top10_s.index:
    descs = df[df['StockCode'] == sc]['Description'].dropna().value_counts()
    desc_map[sc] = descs.index[0] if len(descs) > 0 else 'Unknown'

labels = [f"{sc}\n({desc_map[sc][:22]})" for sc in top10_s.index]

fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
bars = ax.bar(range(10), top10_s.values, color='#ff7f0e', edgecolor='black', alpha=0.85)
ax.set_xticks(range(10))
ax.set_xticklabels(labels, rotation=35, ha='right', fontsize=8.5)
ax.set_title("Figure 4. Top 10 StockCodes by Transaction Line Frequency", fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel("Line Count (Number of Records)", fontsize=10)
ax.set_ylim(0, top10_s.max() * 1.15)
ax.grid(True, linestyle=':', alpha=0.6, axis='y')

for bar, count, pct in zip(bars, top10_s.values, top10_s_pct.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, f"{count:,}\n({pct:.2f}%)", 
            va='bottom', ha='center', fontsize=8, fontweight='bold', color='#222222')

ax.text(0.60, 0.78, f"Total Distinct StockCodes: {df['StockCode'].nunique():,}\nTop 10 Total: {top10_s.sum():,} lines ({top10_s.sum()/total_rows*100:.2f}%)\nCatalog High Dispersion", 
        transform=ax.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="#f8f9fa", ec="#cccccc", alpha=0.95))

plt.tight_layout()
fig.savefig(f"{out_dir}/fig4_stockcode_bar.png", dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# FIG 5: Quantity Boxplot (Full + Focused IQR)
# -------------------------------------------------------------
print("Generating Figure 5: Quantity Boxplots...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

# Full range boxplot
bp1 = ax1.boxplot(df['Quantity'], vert=True, patch_artist=True,
                  boxprops=dict(facecolor='#1f77b4', color='black', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2),
                  whiskerprops=dict(color='black', linewidth=1.2),
                  capprops=dict(color='black', linewidth=1.2),
                  flierprops=dict(marker='o', markerfacecolor='black', markersize=3, alpha=0.3))
ax1.set_title("Full Range Boxplot (Tukey 1.5×IQR Rule)", fontsize=11, fontweight='bold', pad=10)
ax1.set_ylabel("Quantity (Units)", fontsize=10)
ax1.grid(True, linestyle=':', alpha=0.6)

# Focused boxplot [-20, 30]
q_foc_mask = (df['Quantity'] >= -20) & (df['Quantity'] <= 35)
bp2 = ax2.boxplot(df.loc[q_foc_mask, 'Quantity'], vert=True, patch_artist=True,
                  boxprops=dict(facecolor='#2ca02c', color='black', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2, label=f'Median: {df["Quantity"].median():.0f}'),
                  whiskerprops=dict(color='black', linewidth=1.2),
                  capprops=dict(color='black', linewidth=1.2),
                  flierprops=dict(marker='o', markerfacecolor='gray', markersize=2, alpha=0.2))
ax2.set_title("Focused Boxplot View: [-20, 35] Units", fontsize=11, fontweight='bold', pad=10)
ax2.set_ylabel("Quantity (Units)", fontsize=10)

q1_q = df['Quantity'].quantile(0.25)
q3_q = df['Quantity'].quantile(0.75)
iqr_q = q3_q - q1_q
lower_w = q1_q - 1.5 * iqr_q
upper_w = q3_q + 1.5 * iqr_q

ax2.text(0.05, 0.72, f"Q1 (25%): {q1_q:.0f}\nMedian: {df['Quantity'].median():.0f}\nQ3 (75%): {q3_q:.0f}\nIQR: {iqr_q:.0f}\nLower Whisker: {lower_w:.0f}\nUpper Whisker: {upper_w:.0f}\nExtreme Min: {df['Quantity'].min():,}\nExtreme Max: {df['Quantity'].max():,}", 
         transform=ax2.transAxes, fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", alpha=0.95))
ax2.grid(True, linestyle=':', alpha=0.6)

plt.suptitle("Figure 5. Boxplots of Transaction Quantity (North Quay Gifts)", fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
fig.savefig(f"{out_dir}/fig5_quantity_boxplot.png", dpi=300)
plt.close(fig)

# -------------------------------------------------------------
# FIG 6: Price Boxplot (Full + Focused IQR)
# -------------------------------------------------------------
print("Generating Figure 6: Price Boxplots...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

# Full range boxplot
bp1 = ax1.boxplot(df['Price'], vert=True, patch_artist=True,
                  boxprops=dict(facecolor='#9467bd', color='black', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2),
                  whiskerprops=dict(color='black', linewidth=1.2),
                  capprops=dict(color='black', linewidth=1.2),
                  flierprops=dict(marker='o', markerfacecolor='black', markersize=3, alpha=0.3))
ax1.set_title("Full Range Boxplot (Tukey 1.5×IQR Rule)", fontsize=11, fontweight='bold', pad=10)
ax1.set_ylabel("Price (GBP / Unit)", fontsize=10)
ax1.grid(True, linestyle=':', alpha=0.6)

# Focused boxplot [0, 15]
p_foc_mask = (df['Price'] >= 0) & (df['Price'] <= 15)
bp2 = ax2.boxplot(df.loc[p_foc_mask, 'Price'], vert=True, patch_artist=True,
                  boxprops=dict(facecolor='#8c564b', color='black', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2, label=f'Median: £{df["Price"].median():.2f}'),
                  whiskerprops=dict(color='black', linewidth=1.2),
                  capprops=dict(color='black', linewidth=1.2),
                  flierprops=dict(marker='o', markerfacecolor='gray', markersize=2, alpha=0.2))
ax2.set_title("Focused Boxplot View: [£0.00, £15.00] GBP", fontsize=11, fontweight='bold', pad=10)
ax2.set_ylabel("Price (GBP / Unit)", fontsize=10)

q1_p = df['Price'].quantile(0.25)
q3_p = df['Price'].quantile(0.75)
iqr_p = q3_p - q1_p
lower_wp = max(0, q1_p - 1.5 * iqr_p)
upper_wp = q3_p + 1.5 * iqr_p

ax2.text(0.05, 0.72, f"Q1 (25%): £{q1_p:.2f}\nMedian: £{df['Price'].median():.2f}\nQ3 (75%): £{q3_p:.2f}\nIQR: £{iqr_p:.2f}\nLower Bound (1.5 IQR): £{q1_p - 1.5*iqr_p:.2f}\nUpper Whisker: £{upper_wp:.2f}\nExtreme Min: £{df['Price'].min():,.2f}\nExtreme Max: £{df['Price'].max():,.2f}", 
         transform=ax2.transAxes, fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", alpha=0.95))
ax2.grid(True, linestyle=':', alpha=0.6)

plt.suptitle("Figure 6. Boxplots of Unit Price in GBP (North Quay Gifts)", fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()
fig.savefig(f"{out_dir}/fig6_price_boxplot.png", dpi=300)
plt.close(fig)

print("All 6 publication-quality figures successfully created in", out_dir)
