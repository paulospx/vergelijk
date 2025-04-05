import streamlit as st
import logging 
# Initialize logging to log to a rolling file in log directory with a max size of 10 MB and a backup count of 7 files
logging.basicConfig(filename='log/dagelijks.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



st.title("Dagelijks")

files = st.text_area("Enter the list of files to copy (e.g., file1.csv):", "C:\\Repos\\Data\\Curves\\Book_3.xlsx\nC:\\Repos\\Data\\Curves\\Book_2.xlsx")
lines = files.split("\n")

for line in lines:
    if line.strip():  # Check if the line is not empty
        logging.info(f"Processing file: {line.strip()}")

        # If file exists write to log info and display checked otherwise write to log error and display error message
        try:
            with open(line.strip(), 'r') as f:
                logging.info(f"File {line.strip()} exists.")
                st.info(f"✅ File {line.strip()} exists.")
        except FileNotFoundError:
            logging.error(f"File {line.strip()} does not exist.")
            st.error(f"❌ File {line.strip()} does not exist.")
            continue
        except Exception as e:
            logging.error(f"Error processing file {line.strip()}: {e}")
            st.error(f"❌ Error processing file {line.strip()}: {e}")
            continue    

        # Add your file processing logic here
        # For example, you can read the file and display its content or perform any other operation
        # df = pd.read_excel(line.strip())
        # st.write(df.head())`

if st.button("Process File", key=line.strip()):
    # Copy Files to Target
    logging.info(f"File {line.strip()} processed successfully.")
    st.success(f"✅ File {line.strip()} processed successfully.")