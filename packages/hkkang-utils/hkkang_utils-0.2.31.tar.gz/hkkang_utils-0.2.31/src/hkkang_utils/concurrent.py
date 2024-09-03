import functools
import logging
import threading
import traceback
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, List, Optional

from hkkang_utils.list import divide_into_chunks, do_flatten_list


def _shorten_string(text: str) -> str:
    assert isinstance(text, str), f"text must be str type, but {type(text)} is given."
    if len(text) > 10:
        return text[:10] + "..."
    return text


class Thread(threading.Thread):
    """Please use start method to start thread. start method will call run method.
    If you are doing cpu intensive task, please use MultiProcessor class instead of this class. It's much faster.

    Example:
        # Initialize threads
        thread1 = concurrent_utils.Thread(count_million_and_print_name, 1, {"name":"name_1"})
        thread2 = concurrent_utils.Thread(count_million_and_print_name, 2, {"name":"name_2"})

        # Start threads
        thread1.start()
        thread2.start()

        # Wait for threads to finish (this is optional: accessing result will call join method anyway)
        thread1.join()
        thread2.join()

        # Get results
        result1 = thread1.result
        result2 = thread2.result
    """

    # Static variable
    cnt = 0

    def __init__(self, *args, **kwargs):
        super().__init__()
        Thread.cnt += 1
        self.threadID = Thread.cnt
        self.func = args[0]
        self.args = args[1:]
        self.kwargs = kwargs
        self._result = None
        self.logger = logging.getLogger(f"Thread {self.threadID}")

    @property
    def result(self):
        if self.is_alive():
            self.join()
        return self._result

    def run(self):
        post_fix = f"Thread {self.threadID}: {self.func.__name__}(args={_shorten_string(str(self.args))}, kwargs={_shorten_string(str(self.kwargs))})"
        self.logger.info(f"Starting {post_fix}")
        self._result = self.func(*self.args, **self.kwargs)
        self.logger.info(f"Exiting {post_fix}")

    def _parse_args(self, args):
        if args is None:
            return ()
        elif isinstance(args, tuple):
            return args
        elif isinstance(args, list):
            return tuple(args)
        else:
            return (args,)

    def _parse_kwargs(self, kwargs):
        if kwargs is None:
            return {}
        elif isinstance(kwargs, dict):
            return kwargs
        else:
            raise ValueError(f"kwargs must be dict type, but {type(kwargs)} is given.")


class MultiProcessor:
    """
    example:
        # Initialize multi processor
        multiprocessor = Multiprocessor(num_process=4)

        # Run processes concurrently
        multiprocessor.run(count_million_and_print_name, 1, name=f"name_{i}")
        multiprocessor.run(count_million_and_print_name, 2, name=f"name_{i}")
        multiprocessor.run(count_million_and_print_name, 3, name=f"name_{i}")
        multiprocessor.run(count_million_and_print_name, 4, name=f"name_{i}")

        # Wait for all processes to finish (this is optional: accessing result will call join method anyway)
        multiprocessor.join()

        # Get results
        results = multiprocessor.results
    """

    def __init__(self, num_workers: int, store_results: bool = True):
        self.num_workers = num_workers
        self._futures = []
        self._results = []
        self.store_results = store_results
        self.logger = logging.getLogger(f"MultiProcessor")

    @property
    def results(self):
        return self._results

    @functools.cached_property
    def executor(self):
        return ProcessPoolExecutor(max_workers=self.num_workers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        # Clean up: Wait for all processes to finish
        self.join()

        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    def _check_if_valid_function(self, func: Callable):
        if not hasattr(func, "__call__"):
            self.logger.error(
                f"Given function is not callable. Please use callable function."
            )
        elif func.__name__ == "<lambda>":
            self.logger.error(
                f"Given function is lambda function. Please use normal function instead of lambda function."
            )
        else:
            return True
        return False

    def run(self, *args, **kwargs):
        """Pass callable function in the first argument.
        Then, pass other arguments and keyword arguments as you would to the callable function.
        """
        # Extract function and arguments
        assert len(args) > 0, f"Please pass function as the first argument."
        func: Callable = args[0]
        args = args[1:]

        # Check the given function is not lambda function
        self._check_if_valid_function(func)

        self._futures.append(
            self.executor.submit(functools.partial(func, *args, **kwargs))
        )

    def join(self):
        if self.store_results:
            self._results = [future.result() for future in self._futures]
        else:
            for future in self._futures:
                future.result()
        # Free memory
        self.executor.shutdown()


class PartialProcessor:
    """
    This is a class to process data partially.
    Use this class when you want to call multiple programs in terminal to process data in parallel.
    It will split the data and process the data partially considering the total number of processes and the current process number.
    """

    def __init__(
        self,
        func: Optional[Callable] = None,
        total_proc_n: Optional[int] = None,
        current_proc_n: Optional[int] = None,
    ):
        self.func = func
        self.total_proc_n = total_proc_n
        self.current_proc_n = current_proc_n

    def __call__(
        self,
        data: List[Any],
        func: Optional[Callable] = None,
        total_proc_n: Optional[int] = None,
        current_proc_n: Optional[int] = None,
    ) -> List[Any]:
        if func is None:
            func = self.func
        if total_proc_n is None:
            total_proc_n = self.total_proc_n
        if current_proc_n is None:
            current_proc_n = self.current_proc_n
        assert isinstance(
            data, list
        ), f"data must be list type, but {type(data)} is given."
        assert func is not None, f"Please set function to the PartialProcess instance."
        assert (
            total_proc_n is not None
        ), f"Please set total_proc_n to the PartialProcess instance."
        assert (
            current_proc_n is not None
        ), f"Please set current_proc_n to the PartialProcess instance."

        # Divide the data into chunks (each chunk will be processed by each process)
        chunks: List = divide_into_chunks(data, num_chunks=total_proc_n)

        target_chunk = chunks[current_proc_n]
        return func(target_chunk)

    def merge(
        self,
        results: List[Any],
        total_proc_n: Optional[int] = None,
        current_proc_n: Optional[int] = None,
    ) -> List[Any]:
        """Combine results from each process into a list with correct order."""
        if total_proc_n is None:
            total_proc_n = self.total_proc_n
        if current_proc_n is None:
            current_proc_n = self.current_proc_n
        assert (
            total_proc_n is not None
        ), f"Please set total_proc_n to the PartialProcess instance."
        assert (
            current_proc_n is not None
        ), f"Please set current_proc_n to the PartialProcess instance."
        if isinstance(results, list):
            assert type(results[0]) == list, f"results must be list of list type."
            return do_flatten_list(results)
        elif isinstance(results, dict):
            assert (
                type(results[0]) == list
            ), f"value stored in the results dictionary must be list type."
            return [results[i] for i in range(total_proc_n)]
        return results


if __name__ == "__main__":
    pass
