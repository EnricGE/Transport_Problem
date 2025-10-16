class Workshop:
    """
    Workshop class
    
    Attributes
    ----------
    __id_ : str
        Unique identifier of the class instance.
    __production_capacity: float
        Maximum production of the product by the workshop.
    __production_cost: float
        Production cost of the product by the workshop.
    """

    def __init__(
        self, id_: str, production_capacity: float, production_cost: float
    ) -> None:
        self.__id_: str = id_
        self.__production_capacity: float = production_capacity
        self.__production_cost: float = production_cost
    
    @property
    def id_(self) -> str:
        return self.__id_
    
    @id_.setter
    def id_(self, id_: str) -> None:
        self.__id_ = id_
