import logging, os
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, List
from .context import BuildContext, BuildReason

logger = logging.getLogger(__name__)

class SiteStats:
    pages_created: int = 0
    pages_changed: int = 0
    pages_unchanged: int = 0
    pages_deleted: int = 0
    pages_with_errors: int = 0
    pages_are_draft: int = 0
    build_time_seconds: float


class SiteRoot:
    """
    This class represents the root of the site.
    """
    root_path: Final[Path]
    tree: List[BuildContext]

    def __init__(self, path: Path):
        """

        :param path: Path to the root of the site.
        """
        self.root_path = path
        self.tree = []
        self.stats: Final[SiteStats] = SiteStats()

    def make_tree(self) -> None:
        md_dir = self.root_path.joinpath("_public")
        for dir_in, _, files in os.walk(md_dir):
            sub_dir = Path(dir_in)
            for file in files:
                file_path = sub_dir.joinpath(file)
                file_path = file_path.relative_to(md_dir)
                logger.debug("Found page %s", file_path)
                dest = file_path.parent.joinpath(
                    file_path.stem + ".html",
                )
                context = BuildContext(
                    cwd=self.root_path,
                    source=file_path,
                    dest=dest
                )

                match context.build_reason:
                    case BuildReason.CHANGED:
                        self.stats.pages_changed += 1
                    case BuildReason.UNCHANGED:
                        self.stats.pages_unchanged += 1
                    case BuildReason.CREATED:
                        self.stats.pages_created += 1
                    case BuildReason.DELETED:
                        self.stats.pages_deleted += 1


                self.tree.append(context)
