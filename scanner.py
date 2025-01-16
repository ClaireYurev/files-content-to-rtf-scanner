import os

def scan_and_write_to_rtf(output_file):
    excluded_files = {"package-lock.json", "README.md", ".gitignore"}
    excluded_dirs = {"node_modules"}

    with open(output_file, "w", encoding="utf-8") as rtf_file:
        for root, dirs, files in os.walk(os.getcwd()):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            for file in files:
                if file in excluded_files:
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
