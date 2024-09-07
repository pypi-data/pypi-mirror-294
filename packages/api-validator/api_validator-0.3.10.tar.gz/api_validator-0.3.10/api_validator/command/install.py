import click
import platform
from click import echo, style
from click_option_group import optgroup

from api_validator.tools.prerequisites import Prerequisites


@click.command("install", help="Install prerequisites.")
@optgroup.group("Installation Options", help="")
@optgroup.option("--check-only", "-c", is_flag=True, help="Only check if prerequisites are installed.")
@optgroup.option("--force", "-f", is_flag=True, help="Force install prerequisites.")
def install(check_only: bool, force: bool):
    """
    Install prerequisites.
    """
    run_install(check_only, force)


def run_install(check_only: bool, force: bool):
    prerequisites = Prerequisites(force=force)
    prerequisites.validate()
    if not check_only:
        prerequisites.install()

    is_mac = platform.system() == "Darwin"
    if not prerequisites.nightvision_installed:
        if is_mac:
            echo(style("\nnightvision is not installed.", fg="red"))
            echo("To install nightvision, run the following command:")
            echo(style("\tbrew install nvsecurity/taps/nightvision", fg="green"))
        else:
            prerequisites.install_nightvision()
    if not prerequisites.oasdiff_installed:
        if is_mac:
            echo(style("\noasdiff is not installed.", fg="red"))
            echo("\tTo install oasdiff, run the following command:")
            echo(style("\tbrew install tufin/tufin/oasdiff", fg="green"))
        else:
            prerequisites.install_oasdiff()
    # if not prerequisites.github_cli_installed:
    #     if is_mac:
    #         echo(style("\ngithub cli is not installed.", fg="red"))
    #         echo("\tTo install github cli, run the following command:")
    #         echo(style("\tbrew install gh", fg="green"))
    #     else:
    #         prerequisites.install_github_cli()
    # if not prerequisites.semgrep_installed:
    #     if is_mac:
    #         echo(style("\nsemgrep is not installed.", fg="red"))
    #         echo("\tTo install semgrep, run the following command:")
    #         echo(style("\tbrew install semgrep", fg="green"))
    #     else:
    #         prerequisites.install_semgrep()
