import pandas as pd
import plotly.graph_objects as go
import os
import re
import fnmatch

def calculate_differences(df1, df2):
    # New DataFrame to store differences
    dfdelta = pd.DataFrame({"curve_name": [], "percentage": [], "abs_diff_mean": [], "cum_abs_diff": []})
    for col in df1.columns[2:]:
        if col in df2.columns:
            diff = df1[col] - df2[col]
            percentage_diff = (diff / df2[col]) * 100
            abs_diff = abs(diff)           
            dfdelta = pd.concat([dfdelta, pd.DataFrame({"curve_name": [col], "percentage": [percentage_diff.mean()], "abs_diff_mean": [abs_diff.mean()], "cum_abs_diff": [sum(abs(diff))]})], ignore_index=True)
            # Add a column that is cum_abs_diff is 0 then is Equal, else is Not Equal
            dfdelta['is_equal'] = dfdelta['cum_abs_diff'].apply(lambda x: 'Equal' if x == 0 else 'Different')            
            # Sort by name and then by abs difference in descending order
            dfdelta = dfdelta.sort_values(by="curve_name")
            dfdelta = dfdelta.sort_values(by="cum_abs_diff", ascending=False)
    return dfdelta


# Print description for delta
def show_delta_console(df1,df2, file1, file2, sheetname):
    delta = calculate_differences(df1, df2)

    # Create buckets that calculate buckets of 10% for the percentage difference for cum_abs_diff column
    # delta['bucket'] = pd.cut(delta['cum_abs_diff'], bins=[-float('inf'), -10, 0, 10, float('inf')], labels=['< -10%', '0%', '> 0%', '> 10%'])

    print("# Diferences between the columns present in both files")
    print()
    print("The following table shows the differences between the columns present in both files:")
    print(f"- Source: {file1} sheet: {sheetname}")
    print(f"- Target: {file2} sheet: {sheetname}")
    print("The table shows the curve name, percentage difference mean, and absolute differences mean and cumulative absolute difference.")
    print("The table is sorted by the cumulative absolute difference in descending order.")
    print()
    # print the full dataframe to the console
    print()
    print(delta.to_string(index=False))
    print()
    print("---")

    

# Given a path it scans for all the files with and extension and a regex pattern
def get_files(path, extension, pattern):
    files = []
    for file in os.listdir(path):
        if file.endswith(extension) and re.match(pattern, file):
            files.append(os.path.join(path, file))
    return files


# Add a method to plot several curtes in a single plot
def plot_multiple_curves(title, x_values, y_values_list, colors, ui_col, prefix='202501'):
    fig = go.Figure()
    for i, y_values in enumerate(y_values_list):
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name=title[i], line=dict(color=colors[i])))
    fig.update_layout(title=title, xaxis_title='Maturity', yaxis_title='bp', showlegend=True)
    ui_col.plotly_chart(fig)

    try:
        # Create the directory if it doesn't exist
        os.makedirs(f"./img/{prefix}", exist_ok=True)
        fig.write_image(f"./img/{prefix}/diff-{title}.png")
    except Exception as e:
        print(f"Error writing image: {e}")

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
        fig.write_image(f"./img/{prefix}/diff-{title}.png")
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


def append_matching_lines(directory, pattern, search_text, output_file):
    """
    Search for files matching a pattern in a directory, find lines containing specific text,
    and append those lines to an output file.

    Parameters:
        directory (str): Path to the directory to search in.
        pattern (str): Pattern to match file names (e.g., '*.txt').
        search_text (str): Text to search for within files.
        output_file (str): Path to the file where results will be appended.

    Returns:
        None
    """
    try:
        with open(output_file, 'a') as outfile:
            for root, _, files in os.walk(directory):
                for file in fnmatch.filter(files, pattern):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as infile:
                            for line in infile:
                                if search_text in line:
                                    outfile.write(line)
                    except (OSError, UnicodeDecodeError) as e:
                        print(f"Error reading file {file_path}: {e}")
    except OSError as e:
        print(f"Error opening output file {output_file}: {e}")

# Example Usage
# append_matching_lines('path/to/directory', '*.txt', 'search_text', 'output.txt')
