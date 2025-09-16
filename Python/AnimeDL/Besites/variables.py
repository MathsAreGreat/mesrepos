from bs4 import BeautifulSoup
from functools import wraps
from time import sleep


def retry_on_exception(wait_seconds=1):
    """
    A decorator to retry a function if an exception is raised.

    Args:
        wait_seconds (int): Number of seconds to wait before retrying.
    Returns:
        function: A wrapped function with retry logic.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    # Attempt to execute the function
                    result = func(*args, **kwargs)
                    return result
                except Exception:
                    attempts += 1
                    print(f"> Attempt {attempts} failed !")
                    sleep(wait_seconds)

        return wrapper

    return decorator


def monhtml(sess, r, ref=None, data=None):
    if not ref:
        refs = r.split("/")[:3]
        ref = "/".join(refs)
    sess.headers["Referer"] = ref
    if data:
        r = sess.post(r, data=data)
    else:
        r = sess.get(r)
    encoding = (
        r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)
