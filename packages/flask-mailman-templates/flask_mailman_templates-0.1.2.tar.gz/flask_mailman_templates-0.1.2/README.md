# Flask-Mailman-Templates

Templates for [Flask-Mailman](https://waynerv.github.io/flask-mailman)

 - Define your emails as templates
 - Optionnaly use a yaml frontmatter to define metadata like subject
 - Support for markdown emails
 - Support for [MJML](https://mjml.io)
 - Inline css using premailer
 - Optionnaly auto generate text alternative from html emails (if html2text is installed)

## Installation

    pip install flask-mailman-templates

## Usage

Initialize Flask-Mailman first then Flask-Mailman-Templates:

```python
from flask import Flask
from flask_mailman import Mail
from flask_mailman_templates import MailTemplates

app = Flask(__name__)
mail = Mail(app)
mail_templates = MailTemplates(app)
```

Create templates in an email folder. Example `email/hello.txt`:

```
---
subject: Hello world
---
Hello from Flask!
```

Send your email using either `TemplatedEmailMessage` or `send_mail()`:

```python
from flask_mailman_templates import TemplatedEmailMessage, send_mail

msg = TemplatedEmailMessage("hello.txt", "hello@example.com")
msg.send()

# or

send_mail("hello.txt", "hello@example.com")
```

The frontmatter is optionnal and options can be passed as keyword arguments (keyword args override the frontmatter if both are used)

```python
send_mail("hello.txt", "hello@example.com", subject="hello world")
```

## Supported formats

| Format | File extension | Required dependency | Description |
| --- | --- | --- | --- |
| txt | txt | | Text email only |
| HTML | html | | HTML email only |
| Markdown | md | markdown | Text + HTML email |
| [MJML](https://mjml.io) | mjml | mjml | HTML email only |

If [html2text](https://pypi.org/project/html2text/) is installed, HTML emails will be automatically converted to text and both content types will be attached (does not apply to markdown).

## Configuration

| Config key | Extension argument | Description | Default |
| --- | --- | --- | --- |
| MAIL_TEMPLATES_FOLDER | template_folder | Location of email templates | emails |
| MAIL_TEMPLATES_MARKDOWN_OPTIONS | markdown_options | Options for the markdown function | {} |
| MAIL_TEMPLATES_INLINE_CSS | inline_css | Whether to inline css with premailer if installed | True |
| MAIL_TEMPLATES_AUTO_TEXT_BODY_FROM_HTML | auto_text_body_from_html |  Whether to convert HTML content to text content if html2text is installed | True |