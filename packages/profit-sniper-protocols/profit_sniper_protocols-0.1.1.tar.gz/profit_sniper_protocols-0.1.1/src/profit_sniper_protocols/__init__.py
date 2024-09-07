from typing import Literal, Protocol, TypedDict

type Broker = Literal[
    "none", "pineconnector", "profitview", "alpaca", "phemex", "oanda"
]


class ExecutionDefinition(TypedDict, total=True):
    """
    An ExecutionDefinition contains all of the data needed
    for a Broker plugin to execution actions on the said broker platform.
    """

    broker: Broker
    """
        The Broker that is used for execution of commands.
    """

    trade_syntax: str | None
    """
        The trade syntax that is used for submitting the trade.
        This is only used if the broker is "pineconnector" or "profitview".
        Other brokers which use trade_syntax may be added in the future.
    """


class BrokerPlugin(Protocol):
    """
    A broker plugin is a class that is responsible for execution trades
    with a specific broker.
    """

    @property
    def broker(self) -> Broker:
        """
        The broker that the plugin uses for submitting trades.
        """
        ...
