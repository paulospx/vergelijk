import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os
import re

st.set_page_config(page_title="Vergelijken", page_icon="📈", layout="wide")

st.title("Vergelijken")

# Give a title an icon and make streamlit app wide by default
file1 = st.text_input("Enter the first file name (e.g., file1.csv):", "C:\\Repos\\Data\\Curves\\Book_2.xlsx")
file2 = st.text_input("Enter the second file name (e.g., file2.csv):", "C:\\Repos\\Data\\Curves\\Book_3.xlsx")
sheetname = st.selectbox("Select the sheet name:", ["AZ ZC YC", "Sheet1", "Sheet2"])
# 

# Given a path it scans for all the files with and extension and a regex pattern
def get_files(path, extension, pattern):
    files = []
    for file in os.listdir(path):
        if file.endswith(extension) and re.match(pattern, file):
            files.append(os.path.join(path, file))
    return files

# Read the files and store them in a dataframe
df1 = pd.read_excel(file1, sheet_name=sheetname)
df2 = pd.read_excel(file2, sheet_name=sheetname)

# Add a method to plot several curtes in a single plot
def plot_multiple_curves(title, x_values, y_values_list, colors, ui_col):
    fig = go.Figure()
    for i, y_values in enumerate(y_values_list):
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name=title[i], line=dict(color=colors[i])))
    fig.update_layout(title=title, xaxis_title='Maturity', yaxis_title='bp', showlegend=True)
    ui_col.plotly_chart(fig)

def calculate_difference(list1, list2):
    return [a - b for a, b in zip(list1, list2)]    

# Plot a curve chart given a title, list of x values, and list of y values
def plot_curve_chart(title, x_values, y_values, color, ui_col, prefix='202501'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name=title, line=dict(color=color)))
    fig.update_layout(title=title, xaxis_title='Maturity', yaxis_title='bp', showlegend=True)
    ui_col.plotly_chart(fig)
    
    # requires kaleido to be installed to export the image
    # pip install -U kaleido
    
    try:
        # Create the directory if it doesn't exist
        os.makedirs(f"./img/{prefix}", exist_ok=True)
        fig.write_image(f"./img/{prefix}/{title}.png")
    except Exception as e:
        print(f"Error writing image: {e}")

# method to plot a heatmap given a title, list of x values, and list of y values
def plot_heatmap(title, x_values, y_values, color, ui_col):
    fig = go.Figure(data=go.Heatmap(z=y_values, x=x_values, y=x_values, colorscale=color))
    fig.update_layout(title=title, xaxis_title='Curves', yaxis_title='Curves')
    ui_col.plotly_chart(fig)

# Give me a method that given a 2 dataframe, calculartes a correlation matrix and plot it as a heatmap
def plot_correlation_heatmap(df1, df2, title, color, ui_col):
    correlation_matrix = df1.corrwith(df2)
    # sort the correlation matrix by the second column
    sorted_correlation_matrix = correlation_matrix.sort_values(ascending=True)

    fig = go.Figure(data=go.Heatmap(z=sorted_correlation_matrix.values.reshape(1, -1), x=df1.columns, y=['Correlation'], colorscale=color))
    fig.update_layout(title=title, xaxis_title='Curves', yaxis_title='Correlation')
    ui_col.plotly_chart(fig)
    return sorted_correlation_matrix

sorted_corr_matrix = plot_correlation_heatmap(df1.iloc[:, 2:],df2.iloc[:, 2:], 'Correlation Matrix', 'YlGnBu', st)




# select the first column values
maturities = df1.iloc[:, 0].values.tolist()

# select the value from row 3 to row 100 from the first column dataframe
# df1 = df1.iloc[3:100, :]

# how to select the values from 3 to 100 from a list and if the list is smaller than 100, fill with nan
# df1 = df1.iloc[3:100, :].fillna(np.nan)

# add an extra column to sorted correlation matrix with categorization base on the correlation value
sorted_corr_matrix = pd.DataFrame(sorted_corr_matrix)
sorted_corr_matrix['Category'] = pd.cut(sorted_corr_matrix[0], bins=[-1.0, -0.75, -0.50, -0.25, 0.5, 0.75, 0.90, 1], labels=['Stronh Negative','Moderate Negative','Weak Negative','Neutral/Unrelated','Weak Positive', 'Moderate Positive', 'Strong Positive'])
st.table(sorted_corr_matrix)

col1, col2 = st.columns(2)

j = 0
for col in sorted_corr_matrix.index: # df1.columns[2:]:
    compare_category = sorted_corr_matrix.iloc[j, 1]
    col1.subheader(f"{col} Curves")
    col1.markdown(f"**Comparison:** `{compare_category}`")
    try:
        # example of how to use the plot_multiple_curves method
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
