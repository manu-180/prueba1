import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):  # Ajusta esto según los tipos de archivos que quieras monitorear
            print(f'File {event.src_path} has been modified')
            try:
                print('Executing remote_build.ps1...')
                # Usa una ruta absoluta para llamar a remote_build.ps1
                script_path = os.path.join(os.path.dirname(__file__), 'remote_build.ps1')
                result = subprocess.run(['powershell.exe', script_path], shell=True, capture_output=True, text=True)
                print(result.stdout)
                print(result.stderr)
            except Exception as e:
                print(f'Error: {e}')

if __name__ == "__main__":
    print("Starting to watch for file changes...")
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
