from utils.models import Notification
from accounts.models import UserProfile


def create_notification_to_mc_upload(sender, slug, message):
    receivers = UserProfile.objects.filter(
        role=2, faculty=sender.faculty)
    category = 'uploaded_contribution'
    identifier = sender.user.username + "_" + "uploaded_contribution"
    subject = "%s has submitted a new contribution" % sender.get_smallname()
    link = "Contibution Link"
    message_bind = "<h4>%s<h4><br><p>%s</p><br>Click %s to view contribution." % (subject, message, link)
    if receivers.count() > 1:
        for receiver in receivers:
            Notification.objects.create(
                sender=sender,
                receiver=receiver,
                category=category,
                identifier=identifier,
                slug=slug,
                subject=subject,
                message=message_bind
            )
    else:
        Notification.objects.create(
            sender=sender,
            receiver=receivers.first(),
            category=category,
            identifier=identifier,
            slug=slug,
            subject=subject,
            message=message_bind
        )