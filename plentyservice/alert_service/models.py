from typing import Any, Dict, List, Tuple, Union

Alert = Dict[str, Any]
Alerts = List[Alert]
Subscription = Dict[str, Any]
Subscriptions = List[Subscription]
SubscriptionsMap = Dict[str, Subscriptions]
AlertSerials = Union[Tuple[str], List[str]]
