"""
Validate that prerequisites are installed.
"""
import platform

import invoke
from loguru import logger
import platform
from .prerequisite_utils import install_nightvision, install_github_cli


class InstallationError(Exception):
    pass


class Prerequisites:
    def __init__(self, force: bool = False):
        self.openapi_to_postman_installed: bool = False
        self.newman_installed: bool = False
        self.nightvision_installed: bool = False
        self.oasdiff_installed: bool = False
        self.github_cli_installed: bool = False
        self.semgrep_installed: bool = False
        self.force = force

    def validate_openapi_to_postman(self):
        """
        Validate that openapi-to-postman is installed.
        """
        logger.info("Validating that openapi-to-postman is installed...")
        try:
            invoke.run("openapi2postmanv2 --version", hide=True)
            self.openapi_to_postman_installed = True
        except invoke.exceptions.UnexpectedExit:
            self.openapi_to_postman_installed = False
            # logger.warning("openapi2postmanv2 is not installed.")

    def validate_newman(self):
        """
        Validate that newman is installed.
        """
        logger.info("Validating that newman is installed...")
        try:
            invoke.run("newman --version", hide=True)
            self.newman_installed = True
        except invoke.exceptions.UnexpectedExit:
            self.newman_installed = False
            # logger.warning("newman is not installed.")

    def validate_nightvision(self):
        """
        Validate that nightvision is installed.
        """
        logger.info("Validating that nightvision is installed...")
        try:
            invoke.run("nightvision version", hide=True)
            self.nightvision_installed = True
        except invoke.exceptions.UnexpectedExit:
            self.nightvision_installed = False
            # logger.warning("nightvision is not installed.")

    def validate_oasdiff(self):
        """
        Validate that oasdiff is installed.
        """
        logger.info("Validating that oasdiff is installed...")
        try:
            invoke.run("oasdiff --version", hide=True)
            self.oasdiff_installed = True
        except invoke.exceptions.UnexpectedExit:
            self.oasdiff_installed = False
            # logger.warning("oasdiff is not installed.")

    def validate_github_cli(self):
        """
        Validate that GitHub CLI is installed.
        """
        logger.info("Validating that GitHub CLI is installed...")
        try:
            invoke.run("gh --version", hide=True)
            self.github_cli_installed = True
        except invoke.exceptions.UnexpectedExit:
            self.github_cli_installed = False
            logger.warning("GitHub CLI is not installed")

    def validate_semgrep(self):
        logger.info("Validating that semgrep is installed...")
        try:
            invoke.run("semgrep --version", hide=True)
            self.semgrep_installed = True
        except invoke.exceptions.UnexpectedExit:
            self.semgrep_installed = False
            logger.warning("semgrep is not installed")

    @staticmethod
    def install_newman():
        """
        Install newman.
        """
        try:
            invoke.run("npm install -g 'newman@^6.0.0' 'newman-reporter-csv@^1.3.0'", hide=True)
            logger.info("newman installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install newman")
            raise InstallationError(f"Error: {exc.result.stderr}")

    @staticmethod
    def install_openapi_to_postman():
        """
        Install openapi-to-postman.
        """
        try:
            invoke.run("npm install -g openapi-to-postmanv2@^4.18.0", hide=True)
            logger.info("openapi-to-postmanv2 installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install openapi-to-postman.")
            raise InstallationError(f"Error: {exc.result.stderr}")

    @staticmethod
    def install_oasdiff():
        """Install oasdiff"""
        try:
            invoke.run("curl -fsSL https://raw.githubusercontent.com/tufin/oasdiff/main/install.sh | sh", hide=True)
            logger.info("oasdiff installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install oasdiff.")
            raise InstallationError(f"Error: {exc.result.stderr}")

    @staticmethod
    def install_github_cli():
        """Install the GitHub CLI"""
        install_github_cli()

    @staticmethod
    def install_nightvision():
        """
        Install nightvision.
        """
        install_nightvision()

    @staticmethod
    def install_semgrep():
        """Install semgrep"""
        try:
            invoke.run("pip install semgrep --user", hide=True)
            logger.info("semgrep installed.")
        except invoke.exceptions.UnexpectedExit as exc:
            logger.critical("Failed to install semgrep.")
            raise InstallationError(f"Error: {exc.result.stderr}")

    @staticmethod
    def uninstall_openapi_to_postman():
        """
        Uninstall openapi-to-postman.
        """
        try:
            invoke.run("npm uninstall -g openapi-to-postmanv2", hide=True)
        except invoke.exceptions.UnexpectedExit:
            logger.critical("Failed to uninstall openapi-to-postman.")
            raise InstallationError("Failed to uninstall openapi-to-postman.")

    @staticmethod
    def uninstall_newman():
        """
        Uninstall newman.
        """
        try:
            invoke.run("npm uninstall -g newman", hide=True)
        except invoke.exceptions.UnexpectedExit:
            logger.critical("Failed to uninstall newman.")
            raise InstallationError("Failed to uninstall newman.")

    def validate(self):
        """
        Validate prerequisites.
        """
        self.validate_openapi_to_postman()
        self.validate_newman()
        self.validate_nightvision()
        self.validate_oasdiff()
        self.validate_github_cli()
        # self.validate_semgrep()

    def install(self):
        """
        Install prerequisites.
        """
        if not self.newman_installed or self.force:
            self.install_newman()
        if not self.openapi_to_postman_installed or self.force:
            self.install_openapi_to_postman()
        # if not self.nightvision_installed or self.force:
        #     self.install_nightvision()
        # if not self.oasdiff_installed or self.force:
        #     self.install_oasdiff()
        # if not self.github_cli_installed or self.force:
        #     self.install_github_cli()

    def uninstall(self):
        """
        Uninstall prerequisites.
        """
        self.uninstall_newman()
        self.uninstall_openapi_to_postman()
