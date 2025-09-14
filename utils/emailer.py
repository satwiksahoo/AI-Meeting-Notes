# import os, ssl, smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv

# load_dotenv()

# SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
# SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
# SMTP_USER = os.environ.get('SMTP_USER')
# SMTP_PASS = os.environ.get('SMTP_PASS')

# print("SMTP_USER:", SMTP_USER)
# print("SMTP_PASS:", SMTP_PASS)

# HTML_TMPL = """
# <h3>Meeting Summary</h3>
# <h4>Key Points</h4>
# <ul>{key_points}</ul>
# <h4>Decisions</h4>
# <ul>{decisions}</ul>
# <h4>Action Items</h4>
# <ul>{actions}</ul>
# """

# def _li(items):
#     return ''.join([f"<li>{i}</li>" for i in items])


# def _li_actions(items):
#     out = []
#     for it in items:
#         if isinstance(it, dict):
#             owner = it.get('owner','?')
#             task = it.get('task','?')
#             due = it.get('due_date','?')
#             pri = it.get('priority','P2')
#             out.append(f"<li><b>{owner}</b>: {task} (due {due}, {pri})</li>")
#         else:
#             out.append(f"<li>{str(it)}</li>")  # fallback for plain strings
#     return ''.join(out)



# def send_summary(summary, to_emails, subject='Meeting Notes'):
#     if not (SMTP_USER and SMTP_PASS):
#         raise RuntimeError('Set SMTP_USER and SMTP_PASS in environment (or use MailHog).')

#     # Build the message
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     msg['From'] = SMTP_USER
#     msg['To'] = ', '.join(to_emails)

#     # HTML version
#     html = HTML_TMPL.format(
#         key_points=_li(summary.get('key_points', [])),
#         decisions=_li(summary.get('decisions', [])),
#         actions=_li_actions(summary.get('action_items', []))
#     )

#     # Plain-text fallback (safe for dicts + strings)
#     plain_text = "Meeting Summary\n\n"
#     plain_text += "Key Points:\n" + "\n".join(map(str, summary.get('key_points', []))) + "\n\n"
#     plain_text += "Decisions:\n" + "\n".join(map(str, summary.get('decisions', []))) + "\n\n"

#     plain_text += "Action Items:\n"
#     for ai in summary.get('action_items', []):
#         if isinstance(ai, dict):
#             plain_text += f"- {ai.get('owner','?')}: {ai.get('task','?')} (due {ai.get('due_date','?')}, {ai.get('priority','P2')})\n"
#         else:
#             plain_text += f"- {str(ai)}\n"

#     msg.attach(MIMEText(plain_text, 'plain'))
#     msg.attach(MIMEText(html, 'html'))

#     context = ssl.create_default_context()

#     if SMTP_PORT == 465:
#         # SSL mode
#         with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
#             server.login(SMTP_USER, SMTP_PASS)
#             server.sendmail(SMTP_USER, to_emails, msg.as_string())
#     else:
#         # TLS mode (587)
#         with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
#             server.starttls(context=context)
#             server.login(SMTP_USER, SMTP_PASS)
#             server.sendmail(SMTP_USER, to_emails, msg.as_string())


# ------------------------------------------

# def send_summary(summary, to_emails, subject='Meeting Notes'):
#     if not (SMTP_USER and SMTP_PASS):
#         raise RuntimeError('Set SMTP_USER and SMTP_PASS in environment (or use MailHog).')
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     msg['From'] = SMTP_USER
#     msg['To'] = ', '.join(to_emails)
#     html = HTML_TMPL.format(
#         key_points=_li(summary.get('key_points', [])),
#         decisions=_li(summary.get('decisions', [])),
#         actions=_li_actions(summary.get('action_items', []))
#     )
#     msg.attach(MIMEText(html, 'html'))
#     context = ssl.create_default_context()
#     with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
#         server.starttls(context=context)
#         server.login(SMTP_USER, SMTP_PASS)
#         server.sendmail(SMTP_USER, to_emails, msg.as_string())


# def _li_actions(items):
#     out=[]
#     for it in items:
#         owner = it.get('owner','?')
#         task = it.get('task','?')
#         due = it.get('due_date','?')
#         pri = it.get('priority','P2')
#         out.append(f"<li><b>{owner}</b>: {task} (due {due}, {pri})</li>")
#     return ''.join(out)
# ------------------------------------------


import os, ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')

# print("SMTP_USER:", SMTP_USER)
# print("SMTP_PASS:", SMTP_PASS)

HTML_TEMPLATE = """
<h3>Meeting Summary</h3>
<h4>Key Points</h4>
<ul>{key_points}</ul>
<h4>Decisions</h4>
<ul>{decisions}</ul>
<h4>Action Items</h4>
<ul>{actions}</ul>
"""

def _to_li(items):
    """Convert a list of strings to HTML <li> tags"""
    return ''.join(f"<li>{i}</li>" for i in items)

def _actions_to_li(items):
    out = []
    for it in items:
        if isinstance(it, dict):
            owner = it.get('owner','?')
            task = it.get('task','?')
            due = it.get('due_date','?')
            pri = it.get('priority','P2')
            out.append(f"<li><b>{owner}</b>: {task} (due {due}, {pri})</li>")
        else:
            out.append(f"<li>{it}</li>")
    return ''.join(out)

def send_summary(summary, to_emails, subject="Meeting Summary"):
    if not (SMTP_USER and SMTP_PASS):
        raise RuntimeError("SMTP_USER and SMTP_PASS must be set in environment")

    # Build message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(to_emails)

    # HTML & plain-text
    html = HTML_TEMPLATE.format(
        key_points=_to_li(summary.get('key_points', [])),
        decisions=_to_li(summary.get('decisions', [])),
        actions=_actions_to_li(summary.get('action_items', []))
    )
    plain = f"""Meeting Summary

Key Points:
{chr(10).join(summary.get('key_points', []))}

Decisions:
{chr(10).join(summary.get('decisions', []))}

Action Items:
"""
    for ai in summary.get('action_items', []):
        if isinstance(ai, dict):
            plain += f"- {ai.get('owner','?')}: {ai.get('task','?')} (due {ai.get('due_date','?')}, {ai.get('priority','P2')})\n"
        else:
            plain += f"- {ai}\n"

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    # TLS connection
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_emails, msg.as_string())
