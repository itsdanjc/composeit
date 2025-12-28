import os, click, logging, pathlib
from .log import configure_logging
from .site import SiteRoot
from .build import build as build_page

logger = logging.getLogger(__name__)
cwd = pathlib.Path(os.getcwd())


@click.group()
@click.option('--verbose', '-v', is_flag=True, default=False)
def cli(verbose: bool):
    configure_logging(verbose)


@cli.command(help="Build the site.")
@click.option('--force', help="Build all pages, even if unmodified", is_flag=True, default=False)
@click.option("--directory", default=cwd, help="Use the specified directory, instead of the current directory")
def build(force: bool, directory: str):
    """
    Build the site.
    :param force: Build all pages, even if unmodified.
    :param directory: Use the specified directory, instead of the current directory.
    :return: None
    """
    logger.info("Building site at %s.\n", directory)
    directory = pathlib.Path(directory)
    site = SiteRoot(directory)
    site.make_tree()

    logger.info("Found a total of %d pages.", len(site.tree))

    for context in site.tree:
        if context.is_modified or force:
            build_page(context)
            continue

        logger.debug(
            "%s has not been modified since last build. Use --force to overwrite anyway.",
            context.source_path.name
        )

    print_stats(site)


def print_stats(site: SiteRoot) -> None:
    logger.info(
        "\nSuccessfully built %d pages:\n"
        "- %d new page(s)\n"
        "- %d draft page(s)\n"
        "- %d with changes\n"
        "- %d unchanged\n"
        "- %d deleted",
        len(site.tree),
        site.stats.pages_created,
        site.stats.pages_are_draft,
        site.stats.pages_changed,
        site.stats.pages_unchanged,
        site.stats.pages_deleted,
    )

if __name__ == "__main__":
    cli()
