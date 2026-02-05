import os
import sys
import shutil

def clean_directory(directory, ext1, ext2, mode="delete"):
    # Normalize extensions (ensure they start with a dot)
    if not ext1.startswith("."):
        ext1 = "." + ext1
    if not ext2.startswith("."):
        ext2 = "." + ext2

    # Get all files in the directory
    files = os.listdir(directory)

    # Separate files by extension
    files_ext1 = {os.path.splitext(f)[0] for f in files if f.endswith(ext1)}
    files_ext2 = {os.path.splitext(f)[0] for f in files if f.endswith(ext2)}

    # Find common base names
    common = files_ext1 & files_ext2

    # Prepare "to delete" folder if soft delete mode
    to_delete_dir = os.path.join(directory, "to_delete")
    if mode == "soft" and not os.path.exists(to_delete_dir):
        os.makedirs(to_delete_dir)

    # Process files
    for f in files:
        base, ext = os.path.splitext(f)
        if ext in (ext1, ext2) and base not in common:
            file_path = os.path.join(directory, f)

            if mode == "dry":
                print(f"[Dry Run] Would delete: {f}")
            elif mode == "soft":
                shutil.move(file_path, os.path.join(to_delete_dir, f))
                print(f"[Soft Delete] Moved: {f} -> {to_delete_dir}")
            else:  # hard delete
                os.remove(file_path)
                print(f"[Delete] Deleted: {f}")

    print("Cleanup complete!")

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python clean_files.py <directory> <ext1> <ext2> [mode]")
        print("Modes: delete (default), dry, soft")
        print("Example: python clean_files.py /path/to/folder jpg nef dry")
        print("Extensions are case sensitive.")
        sys.exit(1)

    directory = sys.argv[1]
    ext1 = sys.argv[2]
    ext2 = sys.argv[3]
    mode = sys.argv[4] if len(sys.argv) == 5 else "delete"

    clean_directory(directory, ext1, ext2, mode)
