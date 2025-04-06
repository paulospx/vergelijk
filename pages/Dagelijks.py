import streamlit as st
import logging 
import json
import os
import shutil
# Initialize logging to log to a rolling file in log directory with a max size of 10 MB and a backup count of 7 files
logging.basicConfig(filename='log/dagelijks.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# a method to unzip a file
def unzip_file(zip_file, target_folder):
    import zipfile
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(target_folder)
    logging.info(f"Unzipped {zip_file} to {target_folder}")
    st.success(f"✅ Unzipped {zip_file} to {target_folder}")

# a method that generates a list of source, and target files, keeps track of the size and md5 of the copied files
def generate_file_list(source_files, target_folder):
    file_list = ["file1.csv", "file2.csv", "file3.csv"]
    for file in source_files:
        file_info = {
            "source": file,
            "target": f"{target_folder}/{file.split('/')[-1]}",
            "size": 0,
            "md5": ""
        }
        file_list.append(file_info)
    return file_list


# method that exports a list of files to a formatted json file
def export_file_list(file_list, output_file):
    import json
    with open(output_file, 'w') as f:
        json.dump(file_list, f, indent=4)
    logging.info(f"File list exported to {output_file}")
    st.success(f"✅ File list exported to {output_file}")

# method to calculate the md5 hash of a file
def calculate_md5(file_path):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# method that reads plan file and copies the files to the target folder
def copy_files_from_plan(plan_file, target_folder):
    plan = []
    # Read the plan file and load the JSON data
    with open(plan_file, 'r') as f:
        plan = json.load(f)
    for file_info in plan:
        source = file_info["source"]
        target = file_info["target"]
        # Copy the file from source to target

        with st.spinner("Copying files..."):
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            target = os.path.join(target_folder, os.path.basename(source))
            if os.path.exists(target):
                logging.warning(f"File {target} already exists. Skipping copy.")
                st.warning(f"⚠️ File {target} already exists. Skipping copy.")
                continue
            else:
                logging.info(f"Copying {source} to {target}")
                st.info(f"Copying {source} to {target}")
        
        shutil.copy(source, target)
            
        # Update the size and md5 in the plan
        file_info["size"] = os.path.getsize(target)
        file_info["md5"] = calculate_md5(target)
        logging.info(f"Copied {source} to {target}, size: {file_info['size']}, md5: {file_info['md5']}")


monthly_period = st.selectbox("Select the period:", ["202501", "202502", "202503", "202504", "202505", "202506", "202507", "202508", "202509", "202510", "202511", "202512"])
quarterly_period = st.selectbox("Select the quarterly period:", ["2025Q01", "2025Q02", "2025Q03", "2025Q04"])

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

if st.button("Process File", key=line.strip()):
    # Copy Files to Target
    logging.info(f"File {line.strip()} processed successfully.")
    st.success(f"✅ File {line.strip()} processed successfully.")



    


if st.button("Export File List"):
    # Generate file list and export to JSON
    source_files = ["C:\\Repos\\Data\\Curves\\Book_3.xlsx", "C:\\Repos\\Data\\Curves\\Book_2.xlsx", "C:\\Repos\\Data\\Curves\\Book_1.xlsx"]
    target_folder = "C:\\Repos\\Data\\Curves\\Target"
    file_list = generate_file_list(source_files, target_folder)
    output_file = "plan/2025M01_plan.json"
    export_file_list(file_list, output_file)


if st.button("Copy Files"):
    # Copy files from the plan file to the target folder
    plan_file = "plan/2025M01_plan.json"
    target_folder = "C:\\Repos\\Data\\Curves\\Target2025M03"
    copy_files_from_plan(plan_file, target_folder)

    st.markdown(f"Files are available in the target folder. \n```{target_folder}```")
