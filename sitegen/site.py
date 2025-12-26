import logging
from pathlib import Path
from typing import Final, List
from . import BuildContext

logger = logging.getLogger(__name__)

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