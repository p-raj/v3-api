from rest_framework.parsers import BaseParser


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    See: http://www.django-rest-framework.org/api-guide/parsers/#example
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
