from app.extensions import db
from app.models.notification import Notification

def create_notification(
    user_id,
    notification_type,
    title,
    message,
    link=None
):
    """
    Create a notification for a user.
    The calling route is responsible for committing the transaction.
    """

    notification = Notification(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link
    )

    db.session.add(notification)

    return notification