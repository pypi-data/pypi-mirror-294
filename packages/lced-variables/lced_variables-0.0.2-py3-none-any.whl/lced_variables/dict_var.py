import threading


class SingletonDict(dict):
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # 第一重检查：避免在实例已经创建的情况下进行锁操作
        if cls._instance is None:
            with cls._instance_lock:
                # 第二重检查：确保在获取锁后实例仍然没有创建
                if cls._instance is None:
                    cls._instance = super(SingletonDict, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(SingletonDict, self).__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


if __name__ == "__main__":
    single_dict = SingletonDict()
    single_dict["name"] = "linwanlong"
    print(single_dict)
    single_dict_2 = SingletonDict()
    single_dict["age"] = "24"
    print(single_dict)
    print(single_dict["age"])