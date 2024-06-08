from typing import Dict, Any
from rest_framework.serializers import ValidationError


def check_request_to_self(
    data: Dict[str, Any],
    label: str = "friend_request",
    sender: str = "from_user",
    recipient: str = "to_user",
) -> None:
    """
    Check if a friend request is being sent to oneself.
    Args:
        data (Dict[str, Any]): Dict containing sender and recipient info.
        label (str, optional): The label for the ValidationError.
        sender (str, optional): The key for the sender in the dictionary.
        recipient (str, optional): The key for the recipient in the dictionary.
    Raises:
        ValidationError: If the sender and recipient are the same.
    """
    if data[sender] == data[recipient]:
        raise ValidationError({label: "Cannot send request to oneself"})
