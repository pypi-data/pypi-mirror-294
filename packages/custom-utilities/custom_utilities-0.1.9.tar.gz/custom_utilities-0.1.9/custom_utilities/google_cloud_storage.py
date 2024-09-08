import os
import re

from google.cloud import storage
from multiprocessing import cpu_count, Pool
from tqdm import tqdm
from typing import Tuple, Union

def get_gcs_url(gcs_bucket_name:str, gcs_file_path:str) -> str:
    """Return Google Cloud Storage (URL) for given file path in a specific bucket.

    Args:
        gcs_bucket_name (`str`, Mandatory): The name of GCS Bucket which the file exists in.
        gcs_file_path (`str`, Mandatory): The complete path of requested file (must include extension).
    """
    return f"gs://{gcs_bucket_name}/{gcs_file_path}"

def _traverse_local_folder(
    source_folder_path:str,
    bucket_name:str,
    bucket_folder_path:str,
    upload_to_single_folder:bool
) -> list[Tuple[str, str, str]]:
    """Private recursive function to traverse inside a given folder and create upload tasks.

    Args:
        source_folder_path (`str`, Mandatory): path of the folder to be traversed.
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file will be uploaded to.
        bucket_folder_path (`str`, Mandatory): Folder path to which any files in specific folder will be uploaded to in the bucket.
        upload_to_single_folder (`bool`, Optional): Will upload all files inside a folder and all subfolder into a single folder in GCS Bucket.

    Returns:
        `list`: List of download tasks as tuples (bucket_file_path, local_file_path).
    """

    # * Function logic
    entries = list(os.scandir(source_folder_path))
    upload_tasks:list[Tuple] = []
    for entry in entries:
        if entry.is_file():
            if upload_to_single_folder:
                bucket_file_path:str = os.path.join(bucket_folder_path, entry.name)
            else:
                bucket_file_path = re.sub(r'^.*?/', f"{bucket_folder_path}/", entry.path.replace('\\', '/'))
            upload_tasks.append((entry.path, bucket_name, bucket_file_path))
        elif entry.is_dir():
            upload_tasks.extend(_traverse_local_folder(entry.path, bucket_name, bucket_folder_path, upload_to_single_folder))
    return upload_tasks

def _traverse_bucket_folder(
    bucket_name:str,
    bucket_folder_path:str,
    destination_folder_path:str,
    download_to_single_folder:bool
) -> list[Tuple[str, str, str]]:
    """Private function to traverse a folder inside a given GCS folder and create download tasks.

    Args:
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the folder is stored.
        bucket_folder_paths (`str`, Mandatory): The path of the folder in the GCS Bucket.
        destination_folder_path (`str`, Mandatory): The local folder path where files should be saved.
        download_to_single_folder (`bool`, Optional): If True, all files will be downloaded to a single local folder.

    Returns:
        `list`: List of download tasks as tuples (bucket_file_path, local_file_path).
    """

    # * Function Logic
    blobs = storage.Client().bucket(bucket_name).list_blobs(prefix=bucket_folder_path)
    download_tasks = []
    for blob in blobs:
        if blob.name.endswith('/'):
            continue
        if download_to_single_folder:
            local_file_path = os.path.join(destination_folder_path, os.path.basename(blob.name))
        else:
            relative_path = re.sub(f'^{re.escape(bucket_folder_path)}/?', '', blob.name)
            local_file_path = os.path.join(destination_folder_path, relative_path.replace('/', os.path.sep))
        download_tasks.append((bucket_name, blob.name, local_file_path))
    return download_tasks

def _upload_file_to_bucket(source_file_path:str, bucket_name:str, bucket_file_path:str):
    """Private function to upload a single file to a GCS Bucket.

    Args:
        source_file_path (`str`, Mandatory): Path of the to be uploaded file.
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file will be uploaded to.
        bucket_file_path (`str`, Mandatory): Designated path of the uploaded file in the GCS Bucket.
    """

    # * Function Logic
    file_blob = storage.Client().bucket(bucket_name).blob(bucket_file_path)
    if not file_blob.exists():
        file_blob.upload_from_filename(source_file_path)

def _download_file_from_bucket(bucket_name:str, bucket_file_path:str, destination_file_path:str):
    """Private function to download a single file from a GCS Bucket.

    Args:
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file is stored.
        bucket_file_path (`str`, Mandatory): The path of the file in the GCS Bucket.
        destination_file_path (`str`, Mandatory): The local path where the file will be saved.
    """

    # * Function Logic
    file_blob = storage.Client().bucket(bucket_name).blob(bucket_file_path)
    if not file_blob.exists():
        return
    if not os.path.exists(os.path.dirname(destination_file_path)):
        os.makedirs(os.path.dirname(destination_file_path))
    file_blob.download_to_filename(destination_file_path)

def _upload_file_task(args) -> str:
    """Wrapper function for multiprocessing."""
    _upload_file_to_bucket(*args)

def _download_file_task(args) -> str:
    """Wrapper function for multiprocessing."""
    _download_file_from_bucket(*args)

def _process_tasks(
    task_type: str,
    tasks: list[Tuple],
    use_multiprocessing: bool,
    num_workers: int
):
    """Private function to handle processing of tasks (uploading/downloading)."""
    if use_multiprocessing:
        if task_type == 'download':
            task_function = _download_file_task
        elif task_type == 'upload':
            task_function = _upload_file_task
        if os.name == 'nt':
            print('Multiprocessing feature is not yet available for Windows OS in this version.\nFalling back to single-threaded operation.')
            use_multiprocessing = False
        else:
            try:
                num_workers = num_workers if num_workers else cpu_count()
                with Pool(num_workers) as pool:
                    for _ in tqdm(pool.imap_unordered(task_function, tasks), total=len(tasks), desc="Processing files"):
                        pass
            except RuntimeError as e:
                print(f"Multiprocessing failed with error: {e}.\nFalling back to single-threaded operation.")
                use_multiprocessing = False

    if not use_multiprocessing:
        if task_type == 'download':
            task_function = _download_file_from_bucket
        elif task_type == 'upload':
            task_function = _upload_file_to_bucket
        for task in tqdm(tasks, desc="Processing files"):
            task_function(*task)

def upload_file(
    source_file_paths:Union[list[str], str] = None,
    bucket_name:str = None,
    bucket_folder_path:str = None,
    use_multiprocessing:bool = False,
    num_workers:int = None
):
    """Public function to upload a single file or multilpe files to a GCS Bucket.
    If `source_file_paths` is a string (indicating a single file), this will be turned into single-element list.

    Args:
        source_file_paths (`list[str]` or `str`, Mandatory): Path of the to be uploaded file (can be a str for single file or list[str] for multiple files).
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file will be uploaded to.
        bucket_file_path (`str`, Mandatory): Designated folder path of the uploaded file in the GCS Bucket.
        use_multiprocessing (`bool`, Optional): Enables the use of multiprocessing to upload files in parallel, potentially speeding up the upload process. Defaults to `False`.
        num_workers (`int`, Optional): Specifies the number of worker processes to use for multiprocessing. If not set, the default is the number of CPU cores available.

    Raises:
        TypeError: If `source_file_paths` is not a file.
        ValueError: If `source_file_paths`, `bucket_name`, or `bucket_folder_path` is not given.
    """

    # * Function arguments validation
    if not source_file_paths: raise ValueError('Source file paths is not given')
    if isinstance(source_file_paths, str): source_file_paths = [source_file_paths]
    for source_file_path in source_file_paths:
        if not os.path.isfile(source_file_path): raise TypeError(f"'{source_file_path}' is not a file")
    if not bucket_name: raise ValueError('Bucket name is not given')
    if not bucket_folder_path: raise ValueError('Bucket folder path is not given')

    # * Function Logic
    upload_tasks = [(source_file_path, bucket_name, f"{bucket_folder_path}/{os.path.basename(source_file_path)}") for source_file_path in source_file_paths]
    _process_tasks('upload', upload_tasks, use_multiprocessing, num_workers)

def upload_folder(
    source_folder_paths:Union[list[str], str] = None,
    bucket_name:str = None,
    bucket_folder_path:str = None,
    upload_to_single_folder:bool = False,
    use_multiprocessing:bool = False,
    num_workers:int = None
):
    """Public function to upload a single folder or multiple folders and all its contets to a GCS Bucket.
    If `source_folder_paths` is a string (indicating a single folder), this will be turned into single-element list.

    Args:
        source_folder_paths (`list[str]` or `str`, Mandatory): Path of the to be uploaded folder (can be a str for single folder or list[str] for multiple folders).
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the folder will be uploaded to.
        bucket_folder_path (`str`, Mandatory): Designated folder path of the uploaded folder in the GCS Bucket.
        upload_to_single_folder (`bool`, Optional): If True, all files will be uploaded into a single GCS Bucket folder.
        use_multiprocessing (`bool`, Optional): Enables the use of multiprocessing to upload files in parallel. Defaults to `False`.
        num_workers (`int`, Optional): Specifies the number of worker processes to use for multiprocessing. If not set, the default is the number of CPU cores available.

    Raises:
        TypeError: If `source_folder_paths` is not a folder.
        ValueError: If `source_folder_paths`, `bucket_name`, or `bucket_folder_path` is not given.
    """

    # * Function arguments validation
    if not source_folder_paths:
        raise ValueError('Source folder path is not given')
    if isinstance(source_folder_paths, str):
        source_folder_paths = [source_folder_paths]
    for source_folder_path in source_folder_paths:
        if not os.path.isdir(source_folder_path):
            raise TypeError(f"'{source_folder_path}' is not a folder")
    if not bucket_name:
        raise ValueError('Bucket path is not given')
    if not bucket_folder_path:
        raise ValueError('Bucket folder path is not given')
    
    # * Function logic
    upload_tasks:list[Tuple] = []
    for source_folder_path in source_folder_paths:
        upload_tasks.extend(_traverse_local_folder(source_folder_path, bucket_name, bucket_folder_path, upload_to_single_folder))
    _process_tasks('upload', upload_tasks, use_multiprocessing, num_workers)

def download_file(
    bucket_name: str = None,
    bucket_file_paths: Union[list[str], str] = None,
    destination_folder_path: str = '.',
    use_multiprocessing: bool = False,
    num_workers: int = None
):
    """Public function to download file(s) from a GCS Bucket to a local path.

    Args:
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file is stored.
        bucket_file_paths (`list[str]` or `str`, Mandatory): The path(s) of the file(s) in the GCS Bucket.
        destination_folder_path (`str`, Mandatory): The local folder path where the file(s) should be saved.
        use_multiprocessing (`bool`, Optional): Enables the use of multiprocessing to download files in parallel. Defaults to `False`.
        num_workers (`int`, Optional): Specifies the number of worker processes to use for multiprocessing. If not set, the default is the number of CPU cores available.

    Raises:
        ValueError: If `bucket_name`, `bucket_file_paths`, or `destination_folder_path` is not given.
    """

    # * Function arguments validation
    if not bucket_name: raise ValueError('Bucket name is not given')
    if not bucket_file_paths: raise ValueError('Bucket file path is not given')
    if isinstance(bucket_file_paths, str):
        bucket_file_paths = [bucket_file_paths]
    if not destination_folder_path: raise ValueError('Local folder path is not given')

    # * Function Logic
    download_tasks = []
    for bucket_file_path in bucket_file_paths:
        local_file_path = os.path.join(destination_folder_path, os.path.basename(bucket_file_path))
        download_tasks.append((bucket_name, bucket_file_path, local_file_path))
    _process_tasks('download', download_tasks, use_multiprocessing, num_workers)

def download_folder(
    bucket_name:str = None,
    bucket_folder_paths:Union[list[str], str] = None,
    destination_folder_path:str = '.',
    download_to_single_folder:bool = False,
    use_multiprocessing:bool = False,
    num_workers:int = None
):
    """Public function to download a folder and all its contents from a GCS Bucket to a local path.

    Args:
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the folder is stored.
        bucket_folder_paths (`list[str]` or `str`, Mandatory): The path of the folder in the GCS Bucket.
        destination_folder_path (`str`, Mandatory): The local folder path where files should be saved.
        download_to_single_folder (`bool`, Optional): If True, all files will be downloaded to a single local folder.
        use_multiprocessing (`bool`, Optional): Enables the use of multiprocessing to download files in parallel. Defaults to `False`.
        num_workers (`int`, Optional): Specifies the number of worker processes to use for multiprocessing. If not set, the default is the number of CPU cores available.

    Raises:
        ValueError: If `bucket_name`, `bucket_folder_paths`, or `destination_folder_path` is not given.
    """

    # * Function arguments validation
    if not bucket_name: raise ValueError('Bucket name is not given')
    if not bucket_folder_paths: raise ValueError('Bucket folder path is not given')
    if isinstance(bucket_folder_paths, str):
        bucket_folder_paths = [bucket_folder_paths]
    if not destination_folder_path: raise ValueError('Local folder path is not given')

    # * Function logic
    download_tasks: list[Tuple] = []
    for bucket_folder_path in bucket_folder_paths:
        download_tasks.extend(_traverse_bucket_folder(bucket_name, bucket_folder_path, destination_folder_path, download_to_single_folder))
    _process_tasks('download', download_tasks, use_multiprocessing, num_workers)