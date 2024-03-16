import os

# Get the current working directory
cwd = os.getcwd()

# List files in the current directory to find your JSON file
files = os.listdir(cwd)

# Print the list of files to locate your JSON file
print("Files in current directory:", files)

# If you find your JSON file in the list, note its name
# Then construct the absolute path using os.path.join
json_filename = "3.py"  # Replace with your JSON file name
json_abs_path = os.path.join(cwd, json_filename)

# Print the absolute path of your JSON file
print("Absolute path of JSON file:", json_abs_path)
