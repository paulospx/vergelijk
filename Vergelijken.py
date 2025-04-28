import streamlit as st
import numpy as np
import pandas as pd
from utils import show_delta_console, plot_correlation_heatmap, plot_curve_chart, calculate_difference, plot_multiple_curves

st.set_page_config(page_title="Vergelijken", page_icon="📈", layout="wide")

st.title("Vergelijken")

# Give a title an icon and make streamlit app wide by default
file1 = st.text_input("Enter the first file name (e.g., file1.csv):", "C:\\Repos\\Data\\Curves\\Book_2.xlsx")
file2 = st.text_input("Enter the second file name (e.g., file2.csv):", "C:\\Repos\\Data\\Curves\\Book_3.xlsx")
sheetname = st.selectbox("Select the sheet name:", ["AC ZC YC", "Sheet1", "Sheet2"])

# Read the files and store them in a dataframe
df1 = pd.read_excel(file1, sheet_name=sheetname)
df2 = pd.read_excel(file2, sheet_name=sheetname)

show_delta_console(df1, df2,file1, file2, sheetname)

# Name the first column as Maturity and the second column as Currency
df1.columns = ['Maturity', 'Currency'] + df1.columns[2:].tolist()
# df2.columns = ['Maturity', 'Currency'] + df1.columns[2:].tolist()

# Show df1 table with 5 decimal points and 2 decimal points for the first two columns
df1 = df1.round(6)

st.table(df1)


# # join the two dataframes on by 2 columns
# df3 = df1.join(df2.set_index(['Maturity', 'Currency']), on=['Maturity', 'Currency'], rsuffix='_target')
# df3.to_csv('c:/temp/df3.csv', index=False)

sorted_corr_matrix = plot_correlation_heatmap(df1.iloc[:, 2:],df2.iloc[:, 2:], 'Correlation Matrix', 'YlGnBu', st)

# select the first column values
maturities = df1.iloc[:, 0].values.tolist()

# select the value from row 3 to row 100 from the first column dataframe
# df1 = df1.iloc[3:100, :]

# how to select the values from 3 to 100 from a list and if the list is smaller than 100, fill with nan
# df1 = df1.iloc[3:100, :].fillna(np.nan)

# add an extra column to sorted correlation matrix with categorization base on the correlation value
correlation_df = pd.DataFrame({
    'Curve': sorted_corr_matrix.index,
    'Correlation': sorted_corr_matrix.values
}).set_index('Curve')

correlation_df['Category'] = pd.cut(correlation_df['Correlation'], bins=[-1.0, -0.75, -0.50, -0.25, 0.5, 0.75, 0.90, 1], labels=['Strong Negative','Moderate Negative','Weak Negative','Neutral/Unrelated','Weak Positive', 'Moderate Positive', 'Strong Positive'])

# sumarize the number of curves in each category in a dataframe
summary_df = correlation_df.groupby('Category', observed=True).size().reset_index(name='Count')
st.table(summary_df)

# select a list of categories from the correlation_df dataframe excluding nan values  
category = st.selectbox("Select a category:", correlation_df['Category'].unique().dropna().tolist())

# Display the new DataFrame
# st.table(correlation_df) 

# select curves from the selected category
selected_curves = correlation_df[correlation_df['Category'] == category].index.tolist()

sorted_corr_matrix.to_json('./data/202501/sorted_corr_matrix.json', orient='records')

col1, col2 = st.columns(2)

j = 0
for col in selected_curves: # correlation_df.index: 
    compare_category = correlation_df.iloc[j, 1]
    col1.subheader(f"{col} Curves")
    col1.markdown(f"**Comparison:** `{compare_category}`")
    try:
        curves = [df1[col].values.tolist(), df2[col].values.tolist()]
        plot_multiple_curves(col, maturities, curves, ['#D83A34','#61C7D4'], col1)
    except:
        col1.error(f"Error plotting {col} from {file1}. Please check the data.")

    col2.subheader(f"{col} Differences")
    col2.markdown(f"**Comparison:** `{compare_category}`")
    try:
        diff_list = calculate_difference(df1[col].values.tolist(), df2[col].values.tolist())
        plot_curve_chart(col,maturities,diff_list, '#6B66B3', col2)
    except:
        col2.error(f"Error plotting {col} from {file2}. Please check the data.")
    j += 1

