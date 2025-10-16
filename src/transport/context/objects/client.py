class Client:
    """
    Client class

    Attributes
    ----------
    __id_ : str
        Unique identifier of the class instance.
    __demand: float
        Product quantity demand of the product by the client.
    """

    def __init__(self, id_: str, demand: float) -> None:
        self.__id_: str = id_
        self.__demand: float = demand

    @property
    def id_(self) -> str:
        return self.__id_

    @id_.setter
    def id_(self, id_: str) -> None:
        self.__id_ = id_
