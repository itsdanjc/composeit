from pathlib import Path
from datetime import datetime
from marko import Markdown
from marko.block import Document, Heading

BLANK_PAGE_DEFAULT = "# {heading}\n{body}"
ENABLED_MARKO_EXTENSIONS = frozenset(
    {'footnote', 'toc', 'codehilite', 'gfm'}
)


class Page(Markdown):
    """
    Object representing a single page within the site.
    A subclass of `marko.Markdown`.
    """

    title: Heading
    body: Document
    document_path: Path
    is_draft: bool
    default_when_empty: str
    last_modified: datetime

    def __init__(self, path: Path, default: str | None = ""):
        super().__init__(extensions=ENABLED_MARKO_EXTENSIONS)
        self.document_path = path
        self.default_when_empty = BLANK_PAGE_DEFAULT.format(
            heading=self.document_path.stem.title(),
            body=default,
        )

    def read(self) -> None:
        """
        Read and parse the markdown file at located at `self.document_path`.
        :return:
        """
        with self.document_path.open("r", errors='replace') as f:
            self.body = self.parse(f.read())

        if len(self.body.children) == 0:
            self.body = self.parse(self.default_when_empty)

        first_child = self.body.children[0]
        if isinstance(first_child, Heading):
            self.title = first_child
            self.body.children = self.body.children[1:]
