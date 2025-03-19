def find_file_cache():
    import os
    import glob
    import hou  # Houdini module
    """Find all filecache nodes and their cache files across different versions."""
    
    # Get all nodes of type Filecache 2.0 in the scene
    nodes = hou.sopNodeTypeCategory().nodeType("filecache::2.0").instances()

    # Check if there are any such nodes in the scene
    if not nodes:
        hou.ui.displayMessage("No Filecache nodes found in the scene.", title="Warning")
        return  # Exit the function if no nodes are found

    paths = []          # List to store Houdini node paths
    file_paths = []     # List to store paths of the currently selected cache files
    all_cache_files = {}  # Dictionary {node path: list of all cache files}

    # Collect data from each found node
    for node in nodes:
        path = node.path()  # Houdini node path
        cache_path = node.parm("file").eval()  # File path of the selected cache file

        # Expand environment variables (e.g., $JOB, $HIP, etc.)
        expanded_cache_path = hou.expandString(cache_path)
        
        # Get the parent directory of the version folder
        version_folder = os.path.basename(os.path.dirname(expanded_cache_path))  # Extract "v001"
        base_dir = os.path.dirname(os.path.dirname(expanded_cache_path))  # Get "torus" folder
        
        # Search for cache files in all version folders inside "torus"
        search_pattern = os.path.join(base_dir, "*", "*.bgeo.sc")  # Pattern to search inside all versions

        # Find all cache files in the project
        cache_files = glob.glob(search_pattern) if os.path.exists(base_dir) else []

        # Store collected data
        paths.append(path)
        file_paths.append(expanded_cache_path)
        all_cache_files[path] = cache_files  # Store the list of found cache files for this node

    # Print information for debugging
    print("Houdini Node Paths:", paths)
    print("")
    print("File Cache Paths:", file_paths)
    print("")
    print("All Cache Files:", all_cache_files)
    print("")

    # Return data as a dictionary
    return {
        "houdini_paths": paths,
        "file_paths": file_paths,
        "all_cache_files": all_cache_files  # All available cache files
    }
