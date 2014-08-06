from django.template.defaultfilters import truncatechars

from python_imap.folder import INBOX
from lily.messaging.email.models import EmailAccount, EmailMessage
from lily.utils.functions import is_ajax


def email(request):
    """
    Add extra context variables for email.
    """
    extra_context = {}
    extra_context.update(email_auth_update(request))
    extra_context.update(unread_emails(request))
    return extra_context


def email_auth_update(request):
    """
    Add a boolean to the context if there is an email account that needs a new
    password.

    Only check accounts that are editable by the user.
    """
    if request.user.is_anonymous() or is_ajax(request):
        return {}

    if 'email_auth_update' in request.session and request.session['email_auth_update']:
        email_auth_update = True
    else:
        email_auth_update = EmailAccount.objects.filter(
            is_deleted=False,
            auth_ok=False,
            tenant=request.user.tenant,
            user_group__pk=request.user.pk,
        ).exists()

        if email_auth_update:
            request.session['email_auth_update'] = True

    return {'email_auth_update': email_auth_update}


def unread_emails(request):
    """
    Add a list of unread e-mails to the context.
    Limit results with bodies to 10.
    Limit total results to 30.
    """
    if request.user.is_anonymous() or is_ajax(request):
        return {}

    LIMIT_LIST = 10
    LIMIT_EXCERPT = 5
    unread_emails_list = []

    # Look up the last few unread e-mail messages for these accounts
    email_accounts = request.user.get_messages_accounts(EmailAccount)
    email_messages = EmailMessage.objects.filter(
        folder_identifier=INBOX,
        account__in=email_accounts,
        is_seen=False,
    ).order_by('-sort_by_date')
    unread_count = email_messages.count()

    email_messages = email_messages[:LIMIT_LIST]  # eval slice

    # show excerpt for LIMIT_EXCERPT messages
    for email_message in email_messages[:LIMIT_EXCERPT]:
        unread_emails_list.append({
            'id': email_message.pk,
            'from': email_message.from_name,
            'time': email_message.sent_date,
            'message_excerpt': truncatechars(email_message.textify().lstrip('&nbsp;\n\r\n '), 100),
        })

    if len(email_messages) > LIMIT_EXCERPT:
        # for more messages up to LIMIT_LIST don't show excerpt
        for email_message in email_messages[LIMIT_EXCERPT:]:
            unread_emails_list.append({
                'id': email_message.pk,
                'from': email_message.from_name,
                'time': email_message.sent_date,
            })

    return {
        'unread_emails': {
            'count': unread_count,
            'count_more': unread_count - len(unread_emails_list),
            'object_list': unread_emails_list,
        }
    }
