import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

bugs_folder = "megaworld_bugs"
other_folder = "megaworld"
check_folder = "megaworld_check"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        time.sleep(1)  # Wait for file operations to complete
        filename = os.path.basename(event.src_path)
        src_path = os.path.join(check_folder, filename)
        dest_folder = bugs_folder if os.path.getsize(src_path) == 0 else other_folder
        dest_path = os.path.join(dest_folder, filename)
        shutil.move(src_path, dest_path)
        print(f"Moved '{filename}' to {dest_folder}.")
        move_files()  # Run move_files after a new file is created

def move_files():
    if not os.path.exists(bugs_folder):
        print(f"Error: {bugs_folder} folder not found.")
        return
    
    if not os.path.exists(other_folder):
        os.makedirs(other_folder)

if __name__ == "__main__":
    move_files()  # Initial setup
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, check_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
