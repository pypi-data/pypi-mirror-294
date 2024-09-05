import os
from flask import current_app
from jinja2 import Environment, FileSystemLoader, ChoiceLoader
from jinja_frontmatter import RemoveFrontmatterLoader, get_template_frontmatter
from flask_mailman import EmailMultiAlternatives
from dataclasses import dataclass
import markdown
import html2text
from mjml import mjml_to_html
import premailer
import yaml


@dataclass
class MailTemplatesState:
    jinja_env: Environment
    loaders: list
    markdown_options: dict
    inline_css: bool
    auto_text_body_from_html: bool


class MailTemplates:
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, template_folder="emails", inline_css=True, auto_text_body_from_html=True, markdown_options=None):
        choice_loader = ChoiceLoader([FileSystemLoader(os.path.join(app.root_path, app.config.get("MAIL_TEMPLATES_FOLDER", template_folder)))])
        loader = RemoveFrontmatterLoader(choice_loader)
        jinja_env = app.jinja_env.overlay(loader=loader)

        app.extensions["mail_templates"] = MailTemplatesState(
            jinja_env=jinja_env,
            loaders=choice_loader.loaders,
            markdown_options=app.config.get("MAIL_TEMPLATES_MARKDOWN_OPTIONS", markdown_options) or {},
            inline_css=app.config.get("MAIL_TEMPLATES_INLINE_CSS", inline_css),
            auto_text_body_from_html=app.config.get("MAIL_TEMPLATES_AUTO_TEXT_BODY_FROM_HTML", auto_text_body_from_html),
        )


class TemplatedEmailMessage(EmailMultiAlternatives):
    def __init__(self, filename, to, **kwargs):
        ctx, text_body, html_body = render_mail(filename, **kwargs)

        if not ctx.get("subject"):
            raise Exception("Missing subject")

        super().__init__(ctx["subject"], text_body if text_body is not None else html_body, ctx.get("from_email"), to, ctx.get("bcc"),
                         kwargs.get("connection"), None, ctx.get("headers"),
                         ctx.get("cc"), ctx.get("reply_to"))
        
        if text_body is None:
            self.content_subtype = "html"
        elif html_body is not None:
            self.attach_alternative(html_body, "text/html")
        
        relpath = current_app.extensions["mail_templates"].jinja_env.get_template(filename).filename
        for attachment in ctx.get("attachments", []):
            if isinstance(attachment, str):
                self.attach_file(os.path.relpath(attachment, relpath))
            elif isinstance(attachment, (list, tuple)):
                self.attach(*attachment)
            else:
                self.attach(attachment)


def send_mail(filename, to, **kwargs):
    if not isinstance(to, (list, tuple)):
        to = [to]
    message = TemplatedEmailMessage(filename, to, **kwargs)
    message.send()


def render_mail(filename, **ctx):
    state = current_app.extensions["mail_templates"]
    frontmatter = get_template_frontmatter(state.jinja_env, filename, loads=yaml.safe_load)
    if frontmatter:
        for key, value in frontmatter.items():
            if key not in ctx:
                ctx[key] = state.jinja_env.from_string(value).render(**ctx)
    content = state.jinja_env.get_template(filename).render(**ctx)

    _, ext = os.path.splitext(filename)
    text_body = None
    html_body = None
    inline_css = state.inline_css
    if ext == ".mjml":
        result = mjml_to_html(content)
        assert not result.errors
        html_body = result.html
        inline_css = False
    if ext == ".html":
        html_body = content
    elif ext == ".txt":
        text_body = content
    elif ext == ".md":
        text_body = content
        html_body = markdown.markdown(content, **state.markdown_options)

    if html_body and not text_body and state.auto_text_body_from_html:
        text_body = html2text.html2text(html_body)

    if html_body and inline_css:
        html_body = premailer.transform(html_body)

    return ctx, text_body, html_body
