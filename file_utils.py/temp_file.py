import asyncio
import tempfile
import contextlib


def temp_dir():
    """context for creating a temp_dir"""
    return tempfile.TemporaryDirectory()


@contextlib.asynccontextmanager
async def async_save_as_tempfile(file_data: bytes, auto_delete=True):
    """
    write file_data to a temp file

    """
    temp_file = tempfile.NamedTemporaryFile(delete=auto_delete)

    await asyncio.to_thread(temp_file.write, file_data)
    await asyncio.to_thread(temp_file.flush)

    yield temp_file
    await asyncio.to_thread(temp_file.close)


@contextlib.contextmanager
def save_as_tempfile(file_data: bytes, auto_delete=True):
    temp_file = tempfile.NamedTemporaryFile(delete=auto_delete)
    temp_file.write(file_data)
    temp_file.flush()

    yield temp_file

    temp_file.close()
