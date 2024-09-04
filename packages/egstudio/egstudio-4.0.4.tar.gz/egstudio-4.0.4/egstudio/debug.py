from gevent import monkey

monkey.patch_all()

from egstudio.app import app, config
from flask_socketio import SocketIO
import logging
import os
import zipfile
from egstudio.app.utils.commands import dump_database  # Importing the dump_database function


# Configure logging format
FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
socketio = SocketIO(app, cors_allowed_origins=[], cors_credentials=False)


# Function to generate a database backup
def generate_database_backup():
    try:
        # Call dump_database with store=False to generate the backup file
        dump_database(store=False)
        print("Database backup generated successfully.")
    except Exception as e:
        print(f"Error generating database backup: {e}")

# Function to zip the "backups" folder
def zip_folder():
    # Calculate the absolute path of the "backups" folder
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Path to 'egstudio/egstudio'
    folder_path = os.path.join(current_dir, "../previews")  # Navigate to 'egstudio/backups'

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f'Error: Folder "{folder_path}" does not exist.')
        return

    # Create a ZipFile object
    zip_filename = folder_path + '.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the directory and add all files to the zip file
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    print(f'Folder "{folder_path}" zipped successfully.')

# Main entry point
if __name__ == "__main__":
    # Generate the database backup before starting the server
    generate_database_backup()
    zip_folder()

    print("The Kitsu API server is listening on port %s..." % config.DEBUG_PORT)
    socketio.run(app, port=config.DEBUG_PORT, debug=True)
