from typing import Optional

class BuildException(Exception):
    def __init__(self, message: str, *args):
        self.message = message
        super().__init__(args)

class MarkdownParseException(BuildException):
    def __init__(self, message: str, *args):
        super().__init__(message, *args)

class MarkdownRenderException(BuildException):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class MarkdownTemplateException(MarkdownRenderException):
    def __init__(
            self,
            message: str,
            parent_exec_message: Optional[str] = "",
            line_num: Optional[int] = 0,
            template: Optional[str] = ""
    ) -> None:
        self.line_num = line_num
        self.template_source = template
        super().__init__(
            message % (parent_exec_message, line_num, template)
        )