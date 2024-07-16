import os
import json

GIT_USERNAME = "juniorkrz"
GIT_REPO = "Yim-Json-Vehicles-and-Outfits"

def generate_manifest(directory):
    manifest = []

    # Check if the directory exists
    if not os.path.isdir(directory):
        raise ValueError(f'The directory "{directory}" does not exist.')

    # Helper function to recursively traverse directories
    def traverse_directory(current_dir):
        for filename in os.listdir(current_dir):
            file_path = os.path.join(current_dir, filename)

            if os.path.isfile(file_path):
                # If it is a file inside the "files" folder, add it to the manifest
                if current_dir.startswith('./files'):
                    relative_path = os.path.relpath(file_path, directory)
                    relative_path = relative_path.replace(os.sep, '/')
                    file_info = {
                        'filename': filename,
                        'path': os.path.normpath(current_dir),
                        'size': os.path.getsize(file_path),
                        'last_modified': os.path.getmtime(file_path),
                        'download_url': f'https://raw.githubusercontent.com/{GIT_USERNAME}/{GIT_REPO}/master/{relative_path}'
                    }
                    manifest.append(file_info)
            elif os.path.isdir(file_path):
                if filename != '.git':
                    traverse_directory(file_path)


    traverse_directory(directory)

    manifest_file = os.path.join(directory, 'manifest.json')

    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=4)

    print(f'Manifest saved in: {manifest_file}')

if __name__ == '__main__':
    directory_path = './'
    try:
        generate_manifest(directory_path)
    except ValueError as e:
        print(e)
