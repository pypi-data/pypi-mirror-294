from typing import List, Dict, Callable, Any
import random
import string
import abc


class DataGenerators(abc.ABC):
    """
    Abstract class for data generators.
    """

    @staticmethod
    @abc.abstractmethod
    def int_data_generator(n: int) -> List[int]:
        """
        Generate a list of integers.
        """
        return [random.randint(0, 1000) for _ in range(n)]

    @staticmethod
    @abc.abstractmethod
    def str_data_generator(n: int) -> List[str]:
        """
        Generate a list of strings.
        """
        return [string.ascii_lowercase[i % 26] for i in range(n)]

    @staticmethod
    @abc.abstractmethod
    def float_data_generator(n: int) -> List[float]:
        """
        Generate a list of floats.
        """
        return [random.uniform(0, 1000) for _ in range(n)]

    @staticmethod
    @abc.abstractmethod
    def bool_data_generator(n: int) -> List[bool]:
        """
        Generate a list of booleans.
        """
        return [bool(i % 2) for i in range(n)]

    @staticmethod
    @abc.abstractmethod
    def list_data_generator(n: int) -> List[List[int]]:
        """
        Generate a list of lists of integers.
        """
        return [[random.randint(0, 1000) for _ in range(5)] for _ in range(n)]

    @staticmethod
    @abc.abstractmethod
    def dict_data_generator(n: int) -> Dict[str, int]:
        """
        Generate a dictionary of strings and integers.
        """
        return {
            string.ascii_lowercase[i % 26]: random.randint(0, 1000) for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_str_data_generator(n: int) -> Dict[str, str]:
        """
        Generate a dictionary of strings and strings.
        """
        return {
            string.ascii_lowercase[i % 26]: string.ascii_lowercase[i % 26]
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_data_generator(n: int) -> Dict[int, int]:
        """
        Generate a dictionary of integers and integers.
        """
        return {i: random.randint(0, 1000) for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_int_data_generator(n: int) -> Dict[str, int]:
        """
        Generate a dictionary of strings and integers.
        """
        return {
            string.ascii_lowercase[i % 26]: random.randint(0, 1000) for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_str_data_generator(n: int) -> Dict[int, str]:
        """
        Generate a dictionary of integers and strings.
        """
        return {i: string.ascii_lowercase[i % 26] for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_list_data_generator(n: int) -> Dict[str, List[int]]:
        """
        Generate a dictionary of strings and lists of integers.
        """
        return {
            string.ascii_lowercase[i % 26]: [random.randint(0, 1000) for _ in range(5)]
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_list_data_generator(n: int) -> Dict[int, List[int]]:
        """
        Generate a dictionary of integers and lists of integers.
        """
        return {i: [random.randint(0, 1000) for _ in range(5)] for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_data_generator(n: int) -> Dict[str, Dict[str, int]]:
        """
        Generate a dictionary of strings and dictionaries of strings and integers.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: random.randint(0, 1000)
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_data_generator(n: int) -> Dict[int, Dict[int, int]]:
        """
        Generate a dictionary of integers and dictionaries of integers and integers.
        """
        return {i: {j: random.randint(0, 1000) for j in range(5)} for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_float_data_generator(n: int) -> Dict[str, float]:
        """
        Generate a dictionary of strings and floats.
        """
        return {
            string.ascii_lowercase[i % 26]: random.uniform(0, 1000) for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_float_data_generator(n: int) -> Dict[int, float]:
        """
        Generate a dictionary of integers and floats.
        """
        return {i: random.uniform(0, 1000) for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_bool_data_generator(n: int) -> Dict[str, bool]:
        """
        Generate a dictionary of strings and booleans.
        """
        return {string.ascii_lowercase[i % 26]: bool(i % 2) for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_int_bool_data_generator(n: int) -> Dict[int, bool]:
        """
        Generate a dictionary of integers and booleans.
        """
        return {i: bool(i % 2) for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_list_str_data_generator(n: int) -> Dict[str, List[str]]:
        """
        Generate a dictionary of strings and lists of strings.
        """
        return {
            string.ascii_lowercase[i % 26]: [
                string.ascii_lowercase[j % 26] for j in range(5)
            ]
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_list_int_data_generator(n: int) -> Dict[int, List[int]]:
        """
        Generate a dictionary of integers and lists of integers.
        """
        return {i: [j for j in range(5)] for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_str_data_generator(n: int) -> Dict[str, Dict[str, str]]:
        """
        Generate a dictionary of strings and dictionaries of strings and strings.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: string.ascii_lowercase[j % 26]
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_int_data_generator(n: int) -> Dict[int, Dict[int, int]]:
        """
        Generate a dictionary of integers and dictionaries of integers and integers.
        """
        return {i: {j: j for j in range(5)} for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_int_data_generator(n: int) -> Dict[str, Dict[int, int]]:
        """
        Generate a dictionary of strings and dictionaries of integers and integers.
        """
        return {
            string.ascii_lowercase[i % 26]: {j: j for j in range(5)} for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_str_data_generator(n: int) -> Dict[int, Dict[str, str]]:
        """
        Generate a dictionary of integers and dictionaries of strings and strings.
        """
        return {
            i: {
                string.ascii_lowercase[j % 26]: string.ascii_lowercase[j % 26]
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_float_data_generator(n: int) -> Dict[str, Dict[str, float]]:
        """
        Generate a dictionary of strings and dictionaries of strings and floats.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: random.uniform(0, 1000)
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_float_data_generator(n: int) -> Dict[int, Dict[int, float]]:
        """
        Generate a dictionary of integers and dictionaries of integers and floats.
        """
        return {i: {j: random.uniform(0, 1000) for j in range(5)} for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_bool_data_generator(n: int) -> Dict[str, Dict[str, bool]]:
        """
        Generate a dictionary of strings and dictionaries of strings and booleans.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: bool(j % 2) for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_bool_data_generator(n: int) -> Dict[int, Dict[int, bool]]:
        """
        Generate a dictionary of integers and dictionaries of integers and booleans.
        """
        return {i: {j: bool(j % 2) for j in range(5)} for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_list_data_generator(n: int) -> Dict[str, Dict[str, List[int]]]:
        """
        Generate a dictionary of strings and dictionaries of strings and lists of integers.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: [
                    random.randint(0, 1000) for _ in range(5)
                ]
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_list_data_generator(n: int) -> Dict[int, Dict[int, List[int]]]:
        """
        Generate a dictionary of integers and dictionaries of integers and lists of integers.
        """
        return {
            i: {j: [random.randint(0, 1000) for _ in range(5)] for j in range(5)}
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_dict_data_generator(
        n: int,
    ) -> Dict[str, Dict[str, Dict[str, int]]]:
        """
        Generate a dictionary of strings and dictionaries of strings and dictionaries of strings and integers.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: {
                    string.ascii_lowercase[k % 26]: random.randint(0, 1000)
                    for k in range(5)
                }
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_dict_data_generator(
        n: int,
    ) -> Dict[int, Dict[int, Dict[int, int]]]:
        """
        Generate a dictionary of integers and dictionaries of integers and dictionaries of integers and integers.
        """
        return {
            i: {j: {k: random.randint(0, 1000) for k in range(5)} for j in range(5)}
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_dict_str_data_generator(
        n: int,
    ) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Generate a dictionary of strings and dictionaries of strings and dictionaries of strings and strings.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: {
                    string.ascii_lowercase[k % 26]: string.ascii_lowercase[k % 26]
                    for k in range(5)
                }
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_dict_int_data_generator(
        n: int,
    ) -> Dict[int, Dict[int, Dict[int, int]]]:
        """
        Generate a dictionary of integers and dictionaries of integers and dictionaries of integers and integers.
        """
        return {i: {j: {k: k for k in range(5)} for j in range(5)} for i in range(n)}

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_dict_float_data_generator(
        n: int,
    ) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Generate a dictionary of strings and dictionaries of strings and dictionaries of strings and floats.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: {
                    string.ascii_lowercase[k % 26]: random.uniform(0, 1000)
                    for k in range(5)
                }
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_dict_float_data_generator(
        n: int,
    ) -> Dict[int, Dict[int, Dict[int, float]]]:
        """
        Generate a dictionary of integers and dictionaries of integers and dictionaries of integers and floats.
        """
        return {
            i: {j: {k: random.uniform(0, 1000) for k in range(5)} for j in range(5)}
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_str_dict_dict_bool_data_generator(
        n: int,
    ) -> Dict[str, Dict[str, Dict[str, bool]]]:
        """
        Generate a dictionary of strings and dictionaries of strings and dictionaries of strings and booleans.
        """
        return {
            string.ascii_lowercase[i % 26]: {
                string.ascii_lowercase[j % 26]: {
                    string.ascii_lowercase[k % 26]: bool(k % 2) for k in range(5)
                }
                for j in range(5)
            }
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def dict_int_dict_dict_bool_data_generator(
        n: int,
    ) -> Dict[int, Dict[int, Dict[int, bool]]]:
        """
        Generate a dictionary of integers and dictionaries of integers and dictionaries of integers and booleans.
        """
        return {
            i: {j: {k: bool(k % 2) for k in range(5)} for j in range(5)}
            for i in range(n)
        }

    @staticmethod
    @abc.abstractmethod
    def assign_data_generator(func: Callable) -> Callable:
        """
        Assign a data generator to a function.
        """

        def wrapper(n: int) -> Any:
            return func(n)

        return wrapper

    @staticmethod
    @abc.abstractmethod
    def assign_data_generators(funcs: List[Callable]) -> List[Callable]:
        """
        Assign data generators to a list of functions.
        """
        return [DataGenerators.assign_data_generator(func) for func in funcs]
