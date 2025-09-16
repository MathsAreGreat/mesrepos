from pathlib import Path


def delete_empties(*source_directories):
    for source_directory in source_directories:
        nb = 1
        while nb:
            nb = 0
            for source_path in source_directory.rglob("*"):
                if source_path.is_file():
                    continue
                if any(f for f in source_path.glob("*")):
                    continue
                source_path.rmdir()
                nb += 1


def organize_files_by_extension(source_directory):
    """
    Moves files from a source directory into subdirectories named after their extensions.

    Args:
        source_directory (str): The path to the directory to organize.
    """
    if not source_directory.exists():
        print(
            f"Error: Source directory '{source_directory}' does not exist or is not a directory."
        )
        return

    print(f"Organizing files in: {source_directory}")

    # Iterate over all items in the source directory
    for source_path in source_directory.glob("*"):
        # Skip directories, symbolic links, or other non-file types
        if not source_path.is_file():
            continue

        # Get the file extension
        # os.path.splitext returns a tuple: (root, ext)
        file_extension = source_path.suffix

        # Remove the leading dot from the extension (e.g., '.txt' becomes 'txt')
        # If there's no extension (e.g., 'README'), it becomes an empty string.
        # Handle files with no extension by putting them in a '_no_extension' folder
        extension_name = file_extension[
            1:
        ].title()  # Remove dot and convert to lowercase
        # Create the target subdirectory path
        destination_directory = source_directory / f"{extension_name}s"

        # Create the subdirectory if it doesn't exist
        destination_directory.mkdir(parents=True, exist_ok=True)

        # Create the full destination path for the file
        destination_path = destination_directory / source_path.name

        source_path.rename(destination_path)
        print(f"Moved '{source_path.name}' to '{extension_name}/'")

    print(f"Organization complete for {source_directory}.")


def gad_files(*triks):
    for trik in triks:
        for f in trik.rglob("*/*"):
            fn = trik / f.name
            f.rename(fn)
    delete_empties(*triks)
    yt = Path("/home/mohamed/Videos/Youtube")
    for doc in yt.glob("*"):
        name = doc.name
        if "__" not in name:
            continue
        modif = "/".join(name.rsplit("__", 1))
        for f in doc.rglob("*"):
            *parts, fl = f.parts
            parts[parts.index(name)] = modif
            parent = Path(*parts)
            parent.mkdir(parents=True, exist_ok=True)
            f.rename(parent / fl)


# --- How to use the script ---
if __name__ == "__main__":

    source_dir = Path("/home/mohamed/Downloads")
    to = Path("/home/mohamed/Documents/Projects/Backups")
    for f in source_dir.glob("tampermonkey*zip"):
        f.rename(to / f.name)

    source_dir = Path("/home/mohamed/Downloads/Files")
    organize_files_by_extension(source_dir)

    gad_paths = [
        Path("/home/mohamed/Videos/Youtube/Clips"),
        Path("/home/mohamed/Videos/Youtube/Gaza"),
        Path("/home/mohamed/Videos/Youtube/Shorts"),
        *list(Path("/home/mohamed/.Kindas/TikToks").glob("*")),
    ]
    gad_files(*gad_paths)

    delte_paths = [
        source_dir,
        # Path("/home/mohamed/Videos"),
        # Path("/home/mohamed/Music"),
        Path("/home/mohamed/Downloads/Library"),
    ]
    delete_empties(*delte_paths)
