import streamlit as st
import logging 
import json
import os
import shutil
from datetime import datetime
# Initialize logging to log to a rolling file in log directory with a max size of 10 MB and a backup count of 7 files filename timestamped with current date
# Create the log directory if it doesn't exist
if not os.path.exists('log'):
    os.makedirs('log')
   
logging.basicConfig(filename=f"log/dagelijks{datetime.now().strftime('%Y%m%d')}.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

plan_file = "plan/2025M01_plan.json"

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
        
        # if source file does not exist display a warning and skip the copy
        if not os.path.exists(source):
            logging.error(f"Source file {source} does not exist. Skipping copy.")
            st.error(f"❌ Source file {source} does not exist. Skipping copy.")
            continue
        else:
            # Copy the file from source to target
            shutil.copy(source, target)
            
        # Update the size and md5 in the plan
        file_info["size"] = os.path.getsize(target)
        file_info["md5"] = calculate_md5(target)
        logging.info(f"Copied {source} to {target}, size: {file_info['size']}, md5: {file_info['md5']}")

st.title("Dagelijks")

col1, col2 = st.columns(2)

monthly_period = col1.selectbox("Select the period:", ["202501", "202502", "202503", "202504", "202505", "202506", "202507", "202508", "202509", "202510", "202511", "202512"])
quarterly_period = col2.selectbox("Select the quarterly period:", ["2025Q01", "2025Q02", "2025Q03", "2025Q04"])


# Read the plan file to a string with indented 4 space JSON
with open(plan_file, 'r') as f:
    plan_content = json.dumps(json.load(f), indent=4)
    st.code(plan_content, language='json', height=300)


if st.button("Verify Source Files"):
    plan = []
    # Read the plan file and load the JSON data
    with open(plan_file, 'r') as f:
        plan = json.load(f)
    for file_info in plan:
        source = file_info["source"]
        
        # verify the source file exists
        if os.path.exists(source): 
            logging.info(f"Source file {source} exists.")
            st.success(f"✅ Source file {source} exists.")
        else:
            logging.error(f"Source file {source} does not exist.")
            st.error(f"❌ Source file {source} does not exist.")


        # if st.button("Process File", key=line.strip()):
        #     # Copy Files to Target
        #     logging.info(f"File {line.strip()} processed successfully.")
        #     st.success(f"✅ File {line.strip()} processed successfully.")

if st.button("Verify Target Folder"):
    target_folder = st.text_input("Enter the target folder:", "C:\\Repos\\Data\\Curves\\Target2025M03")
    if os.path.exists(target_folder):
        logging.info(f"Target folder {target_folder} exists.")
        st.info(f"✅ Target folder {target_folder} exists.")
    else:
        logging.error(f"Target folder {target_folder} does not exist.")
        st.error(f"❌ Target folder {target_folder} does not exist.")	


if st.button("Copy Files"):
    # Copy files from the plan file to the target folder
    
    target_folder = "C:\\Repos\\Data\\Curves\\Target2025M03"
    copy_files_from_plan(plan_file, target_folder)

    st.markdown(f"Files are available in the target folder. \n```{target_folder}```")


