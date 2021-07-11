import os
import shutil
from queue import Queue
from threading import Thread


def copy(queue: Queue,
         from_path: list,
         to_path: str
         ) -> None:
    """Copies files/folders from source path to destination path.
    Args:
        queue: A queue where it puts and gets files. It's limited according to input value.
        from_path: An array of files' or folders' source paths.
        to_path: A destination path.
    Raises:
        NameError: No such files or folders.
    """
    if len(from_path) > 1:  # In case files were got with mask
        for single_path in from_path:
            file = os.path.basename(os.path.normpath(single_path))
            files_location = os.path.commonpath(from_path)
            queue.put(file)
            Thread(target=copy_file, args=(queue, files_location, to_path)).start()
        print('Files have been copied.')
    else:  # In other cases there will be just one item in array
        source_location = from_path[0]
        if os.path.isdir(from_path[0]):
            files = os.listdir(source_location)
            folder_name = os.path.basename(os.path.normpath(source_location))
            path_to_folder = os.path.join(to_path, folder_name)

            if not os.path.exists(path_to_folder):
                os.mkdir(path_to_folder)

            for file in files:
                # Each file we put to a queue that has limited number of items.
                # And than it creates a separate thread for each file.
                queue.put(file)
                Thread(target=copy_file, args=(queue, source_location, path_to_folder)).start()
            print('Folder has been copied.')
        elif os.path.isfile(from_path[0]):  # If it's a file we just copy it without any threads
            file_name = os.path.basename(os.path.normpath(source_location))
            if not os.path.exists(file_name):
                shutil.copy(source_location, to_path)
                print(f'File {file_name} has been copied.')
            else:
                print(f'File {file_name} already exists')
        elif not os.path.exists(from_path[0]):
            raise NameError('No such files or folders.')


def copy_file(queue: Queue, from_path: str, to_path: str) -> None:
    file = queue.get()
    file_from_path = os.path.join(from_path, file)
    file_to_path = os.path.join(to_path, file)
    shutil.copy(file_from_path, file_to_path)


def move(queue: Queue,
         from_path: list,
         to_path: str
         ) -> None:
    """Moves files/folders from source path to destination path.
        Args:
            queue: A queue where it puts and gets files. It's limited according to input value.
            from_path: An array of files' or folders' source paths.
            to_path: A destination path.
        Raises:
            NameError: No such files or folders.
        """
    if len(from_path) > 1:  # In case files were got with mask
        for single_path in from_path:
            file = os.path.basename(os.path.normpath(single_path))
            files_location = os.path.commonpath(from_path)
            queue.put(file)
            Thread(target=move_file, args=(queue, files_location, to_path)).start()
        print('Files have been moved.')
    else:  # In other cases there will be just one item in array
        source_location = from_path[0]
        if os.path.isdir(from_path[0]):
            files = os.listdir(source_location)
            folder_name = os.path.basename(os.path.normpath(source_location))
            path_to_folder = os.path.join(to_path, folder_name)

            if not os.path.exists(path_to_folder):
                os.mkdir(path_to_folder)

            threads = []
            for file in files:
                # Each file we put to a queue that has limited number of items.
                # And than it creates a separate thread for each file.
                queue.put(file)
                move_thread = Thread(target=move_file, args=(queue, source_location, path_to_folder))
                threads.append(move_thread)
                move_thread.start()
            # Make sure that all our thread are finished before removing original folder
            for thread in threads:
                thread.join()

            os.rmdir(source_location)
            print('Folder has been moved.')
        elif os.path.isfile(from_path[0]):  # If it's a file we just copy it without any threads
            file_location = from_path[0]
            file_name = os.path.basename(os.path.normpath(file_location))
            if not os.path.exists(file_name):
                shutil.move(file_location, to_path)
                print(f'File {file_name} has been moved.')
            else:
                print(f'File {file_name} already exists')
        elif not os.path.exists(from_path[0]):
            raise NameError('No such files or folders.')


def move_file(queue: Queue, from_path: str, to_path: str) -> None:

    file = queue.get()
    file_from_path = os.path.join(from_path, file)
    file_to_path = os.path.join(to_path, file)
    shutil.move(file_from_path, file_to_path)


# Dict with all our available operations
operations = {
    'copy': copy,
    'move': move
}
