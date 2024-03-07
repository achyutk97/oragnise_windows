import re
import os

def find_file(file_name_regex, directory):
  """Recursively searches for a file in a directory and all its subdirectories that matches the given regular expression.

  Args:
    file_name_regex: A regular expression to match the file name.
    directory: The directory to start searching from.

  Returns:
    A list of all the full paths to the files that match the regular expression.
  """

  file_paths = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if re.match(file_name_regex, file):
        file_paths.append(os.path.join(root, file))

  return file_paths

# Example usage:

file_name_regex = r"(.*)(BOXN)(.*).wag$"
directory = r"E:\DCIM\Train Simulator\TRAINS\TRAINSET"

file_paths = find_file(file_name_regex, directory)

train_data = []
if file_paths:
  for file_path in file_paths:
    print(f"Found file at: {file_path}")
    file = file_path.split("\\")
    train_data.append((file[-1], file[-2]))
else:
  print("No files found.")
  
for i in train_data:
    print(i)