import io
import numpy as np

def ndarray_to_bytes(array: np.ndarray) -> bytes:
    """
    Encode a `np.ndarray` to bytes in `.npy` format and return the bytes.
    """
    bio = io.BytesIO()
    np.save(bio, array, allow_pickle=False)
    return bio.getvalue()


def bytes_to_ndarray(b: bytes) -> np.ndarray:
    """
    Given the bytes for a `.npy` formatted file, return the `np.ndarray` data
    """
    bio = io.BytesIO(b)
    return np.load(bio)
