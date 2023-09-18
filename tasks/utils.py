
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .consumers import RealTimeUpdatesConsumer


# Trigger an update event whenever there's a change
async def trigger_update(user):
    channel_layer = get_channel_layer()
    data = RealTimeUpdatesConsumer.get_recent_data(user)
    await channel_layer.group_send(
        f"user_{user.id}",
        {
            "type": "send_updates",
            "data": data,
        }
    )
