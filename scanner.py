import os

def read_gitignore():
    gitignore_files = set()
    try:
        with open(".gitignore", "r", encoding="utf-8") as gitignore:
            for line in gitignore:
                line = line.strip()
                if line and not line.startswith("#"):
                    gitignore_files.add(line)
    except FileNotFoundError:
        pass
    return gitignore_files

def should_exclude(path, excluded_patterns):
    for pattern in excluded_patterns:
        if os.path.commonpath([path, pattern]) == pattern or path.endswith(pattern):
            return True
    return False

def scan_and_write_to_rtf(output_file):
    excluded_files = {"package-lock.json", "README.md", ".gitignore"}
    excluded_dirs = {"node_modules", ".git"}

    # Include patterns from .gitignore
    gitignore_patterns = read_gitignore()

    with open(output_file, "w", encoding="utf-8") as rtf_file:
        for root, dirs, files in os.walk(os.getcwd()):
            # Exclude directories from .gitignore and predefined excluded_dirs
            dirs[:] = [d for d in dirs if d not in excluded_dirs and not should_exclude(os.path.join(root, d), gitignore_patterns)]

            for file in files:
                if file in excluded_files or should_exclude(os.path.join(root, file), gitignore_patterns):
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, os.getcwd())

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        contents = f.read()

                    # Write to the .rtf file in the specified format
                    rtf_file.write(f"// Contents of \"{relative_path}\"\n")
                    rtf_file.write(contents)
                    rtf_file.write("\n\n")
                except (UnicodeDecodeError, PermissionError) as e:
                    print(f"Skipping file {relative_path} due to error: {e}")

if __name__ == "__main__":
    output_filename = "output.rtf"
    scan_and_write_to_rtf(output_filename)
    print(f"All contents written to {output_filename}.")
