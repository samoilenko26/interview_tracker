from fastapi import APIRouter

from interview_tracker.web.api.echo.schema import Message

router = APIRouter()


@router.post("/", response_model=Message)
async def send_echo_message(
    incoming_message: Message,
) -> Message:
    """
    Sends echo back to users.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """
    return incoming_message
