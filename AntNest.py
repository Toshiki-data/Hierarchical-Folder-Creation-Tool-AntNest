import os
import sys
import re

file_path = "AntNest.txt"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

paths = [""]
depth_set = 0

with open("AntNest_log.txt", "w", encoding="utf-8") as log:

    # Processing the first line
    paths[0] = lines[0].strip()

    ## Check if the target folder already exists
    if not os.path.exists(paths[0]):
        message = f"⚠️ Failure: Destination path does not exist.\n"
        log.write(message)
        sys.exit()

    # Processing lines from the second onward
    for line in lines[1:]:

        ## Skip the loop if the line is blank
        if not line.strip():
            continue

        ## Remove trailing spaces from the folder name
        folder_name_wTabL = line.rstrip()

        ## Check if the folder name contains tabs (terminate with an error if so, to avoid processing issues)
        if re.search(r'\t', folder_name_wTabL.lstrip()):
            message = f"⚠️ Failure: Tab found in a folder name.\n"
            log.write(message)
            sys.exit()

        ## Count the number of leading tabs in the folder name
        depth_current = folder_name_wTabL.count("\t") + 1

       ## Remove leading spaces from the folder name
        folder_name = folder_name_wTabL.lstrip()

        ## If the folder level is deeper than the previous
        if depth_current > depth_set:

            if depth_current - depth_set > 1:
                message = f"⚠️ Failure: Depth bigger than 1.\n"
                log.write(message)
                sys.exit()

            paths.append(folder_name)
            depth_set = depth_current

        ## If the folder level is shallower than the previous
        elif depth_current < depth_set:
            gap = depth_set - depth_current

            for i in range(gap + 1):
                paths.pop()

            paths.append(folder_name)
            depth_set = depth_current

        ## If the folder level remains the same
        else:
            paths.pop()
            paths.append(folder_name)

        ## Combine the folder name with elements from the list based on the current hierarchy level
        directory = os.path.join(*paths[:depth_set + 1])

        try:
            os.makedirs(directory, exist_ok=True)
            message = f"✅ Success: {directory}\n"
            log.write(message)

        except Exception as e:
            message = f"⚠️ Failure: {directory}\nReason: {e}\n"
            log.write(message)

