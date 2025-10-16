class Route:
    """
    Route class

    Attributes
    ----------
    __origin : str
        Origin Workshop of the route.
    __destination : str
        Destination Workshop of the route.
    __transport_cost: float
        Cost to transport the product through the route.
    __transport_capacity: float
        Maximum product capacity to transport through the route.
    __is_active: bool
         Boolean indicating whether the route is active.
    """

    def __init__(
        self,
        origin: str,
        destination: str,
        transport_cost: float,
        transport_capacity: float,
        is_active: bool,
    ) -> None:
        self.__origin: str = origin
        self.__destination: str = destination
        self.__transport_cost: float = transport_cost
        self.__transport_capacity: float = transport_capacity
        self.__is_active: bool = is_active

    # --- ID made of (origin, destination)
    @property
    def identifier(self) -> tuple[str, str]:
        return (self.__origin, self.__destination)

    @property
    def origin(self) -> str:
        return self.__origin

    @property
    def destination(self) -> str:
        return self.__destination

    @property
    def transport_cost(self) -> float:
        return self.__transport_cost

    @transport_cost.setter
    def transport_cost(self, value: float) -> None:
        self.__transport_cost = float(value)

    @property
    def transport_capacity(self) -> float:
        return self.__transport_capacity

    @transport_capacity.setter
    def transport_capacity(self, value: float) -> None:
        self.__transport_capacity = float(value)

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self.__is_active = bool(value)
