#!/bin/zsh

# This script recursively replaces spaces with underscores in file and directory names.
#
# Created from Google Overview AI prompt of...  
# create a zsh script to recursively change and count all embedded spaces to underscores in file paths

# Usage: Navigate to the directory tree root and `~/GitHub/Flet-Create-Image-Derivatives/rename-file-paths-no-spaces.zsh``

# Enable globstar for recursive directory traversal
# setopt globstar

# Initialize a counter for changes
local changes_made=0

# Loop through all files and directories recursively
for path in **/*(N); do
  # Check if the path contains spaces
  if [[ "$path" == *" "* ]]; then
    # Create the new path with spaces replaced by underscores
    local new_path="${path// /_}"

    # Rename the file/directory
    /bin/mv -v "$path" "$new_path"
    
    # Increment the counter
    ((changes_made++))
  fi
done

echo "Finished renaming. Total changes made: $changes_made"