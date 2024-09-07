import asyncio
import os
import importlib.util
import sys
import inspect
import git
import re
import subprocess

from typing import Optional
from logging import getLogger

from pyrogram import Client

from tassistant_bot.helpers import I18n, SingletonMeta
from tassistant_bot.helpers.i18n import get_locales

logger = getLogger(__name__)
_ = I18n("ru")


def load_module(directory: str, module_name: str):
    """
    Loads a Python module from the specified directory.

    :param directory: The directory where the module is located.
    :param module_name: The name of the module to be loaded.
    :return: The loaded module.
    """
    module_path = os.path.join(directory, f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_directory_modules(directory_path: str):
    """
    Loads all Python modules from the specified directory.

    :param directory_path: The path of the directory containing modules.
    :return: A dictionary where keys are module names and values are the loaded modules.
    """
    modules = {}
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module = load_module(directory_path, module_name)
                modules[module_name] = module
    return modules


class Module:
    """
    A base class for defining modules (plugins) of Tassistant user bot.

    :param base_path: The base directory path where the module is located.
    """

    class Meta:
        """
        Metadata for the module.
        """

        name = None
        description = None
        requirements = None
        module_name = None

    def __init__(self, base_path: str) -> None:
        """
        :param base_path: The base directory path where the module is located.
        """
        self.base_path = base_path
        self.commands = {}
        self.handlers = {}
        self.scenarios = {}
        self.locale = {}

    def load_locale(self) -> None:
        """
        Loads the locale files for the module and updates the localization.
        """
        locale_path = os.path.join(self.base_path, "locale")
        locales = get_locales(locale_path)
        _.update_locales(locales, self.Meta.module_name)

    def load_services(self) -> None:
        """
        Loads service modules from the 'services' directory.
        """
        scenarios_path = os.path.join(self.base_path, "services")
        self.scenarios = load_directory_modules(scenarios_path)

    def load_handlers(self) -> None:
        """
        Loads handler modules from the 'handlers' directory and registers them.
        """
        handlers_path = os.path.join(self.base_path, "handlers")
        handlers = load_directory_modules(handlers_path)
        for module_name, module in handlers.items():
            try:
                self.handlers[module_name] = module.all_handlers
            except AttributeError:
                logger.error(
                    f"| Handlers | {module_name} | Not found <all_handlers> list"
                )
                raise Exception(
                    f"| Handlers | {module_name} | Not found <all_handlers> list"
                )

    def register_handlers(self, client: Client) -> None:
        """
        Registers handlers with the Pyrogram client.

        :param client: The Pyrogram client instance.
        """
        for module_name, module in self.handlers.items():
            try:
                for handler in module:
                    client.add_handler(handler)
                    logger.info(
                        f"| {self.Meta.name} | {handler.callback.__name__} | Loaded "
                    )
            except Exception as e:
                logger.error(f"| {module_name} | Not Loaded due to error |\n{e} ")

    async def client_ready(self, client: Client) -> None:
        """
        Prepares the module by loading locale, handlers, and services, and registers handlers.

        :param client: The Pyrogram client instance.
        """
        sys.path.append(self.base_path)
        self.load_locale()
        self.load_handlers()
        self.load_services()
        self.register_handlers(client)

    def on_unload(self, client: Client) -> None:
        """
        Unloads the module by removing registered handlers.

        :param client: The Pyrogram client instance.
        """
        for module_name, module in self.handlers.items():
            try:
                for handler in module:
                    client.remove_handler(handler)
                    logger.info(
                        f"| {self.Meta.name} | {handler.callback.__name__} | Unloaded "
                    )
            except Exception as e:
                logger.error(f"| {module_name} | Not Unloaded due to error |\n{e} ")


def extract_repo_name(url: str) -> Optional[str]:
    """
    Extracts the repository name from a GitHub URL.

    :param url: The URL of the GitHub repository.
    :return: The repository name if extracted, otherwise None.
    """
    pattern = r"github\.com/[^/]+/([^/]+)\.git$"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


class ModuleLoader(metaclass=SingletonMeta):
    """
    Module Manager of Tassistant modules

    :param modules_dir: Directory containing the modules.
    :param command_prefix: Command prefix for the module commands.
    :param client: The Pyrogram client instance.
    """

    def __init__(
        self,
        modules_dir: str = "modules",
        command_prefix: str = "/",
        client: Client = None,
    ) -> None:
        if not client:
            logger.error("| ModuleLoader | CLIENT NOT PROVIDED !!! |")
            raise Exception("| CLIENT NOT PROVIDED !!! |")

        self.command_prefix = command_prefix
        self.client = client
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.modules_dir = os.path.join(current_dir, modules_dir)
        self.modules = {}

    def get_command_prefix(self) -> str:
        """
        Returns the command prefix used for the module commands.

        :return: The command prefix.
        """
        return self.command_prefix

    def download_module(self, repo_url: str, to_dir: Optional[str] = None) -> None:
        """
        Downloads a module from a GitHub repository.

        :param repo_url: The URL of the GitHub repository.
        :param to_dir: Optional directory to clone the repository into. Defaults to the modules directory.
        """

        repo_name = extract_repo_name(repo_url)
        if not to_dir:
            to_dir = os.path.join(self.modules_dir, repo_name)
        else:
            to_dir = os.path.join(self.modules_dir, to_dir)
        if os.path.exists(to_dir):
            return
        try:
            git.Repo.clone_from(repo_url, to_dir)

            requirements_path = os.path.join(to_dir, "requirements.txt")

            if os.path.exists(requirements_path):
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-r", requirements_path]
                )
                logger.info(
                    f"| {repo_name} | Installed dependencies from requirements.txt"
                )
            logger.info(f"| {repo_name} | Downloaded to {to_dir}")
        except git.exc.GitError as e:
            logger.error(f"| {repo_name}| {e}")
            raise e

    def load_module(self, module_name: str, module_path: Optional[str] = None) -> None:
        """
        Loads a module by name and path.

        :param module_name: The name of the module.
        :param module_path: Optional path to the module directory. Defaults to the modules directory.
        """
        try:
            if not module_path:
                modules_dir = self.modules_dir
                module_base_path = os.path.join(modules_dir, module_name)
                module_main_path = os.path.join(module_base_path, "module.py")
            else:
                modules_dir = module_path
                module_base_path = module_path
                module_main_path = os.path.join(module_base_path, "module.py")

            spec = importlib.util.spec_from_file_location("module.py", module_main_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            mod_instance = None
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Module) and obj != Module:
                    mod_instance = obj(module_base_path)
                    self.modules[module_name] = mod_instance
                    break

            if mod_instance:
                asyncio.create_task(mod_instance.client_ready(self.client))
        except Exception as e:
            logger.error(f"Error loading module {module_name}\n {e}")

    def update_all(self) -> None:
        """
        Checks for updates in all Git repositories, pulls changes if any, and reloads the modules.
        """
        for module_name in list(self.modules.keys()):
            try:
                self.update_module(module_name)
            except git.exc.GitError as e:
                logger.error(f"| {module_name} | {e}")
                continue

    def update_module(self, module_name):
        if module_name not in self.modules.keys():
            repo_path = os.path.join(self.modules_dir, module_name)
        else:
            module = self.modules[module_name]
            repo_path = module.base_path

        updated = False

        if os.path.exists(os.path.join(repo_path, ".git")):
            try:
                repo = git.Repo(repo_path)
                current = repo.head.commit

                origin = repo.remotes.origin
                origin.fetch()
                origin.pull()

                if current != origin.repo.head.commit:
                    logger.info(f"| {module_name} | Updated successfully.")
                    updated = True
                else:
                    logger.info(f"| {module_name} | No updates found.")
            except git.exc.GitError as e:
                logger.error(f"| {module_name} | Git error: {e}")

        if updated:
            self.unload_module(module_name)
            self.load_modules(module_name)

    def load_modules(self, module_name: str) -> None:
        """
        Loads all modules within a specified module directory.

        :param module_name: The name of the top-level module directory.
        """
        module_base_path = os.path.join(self.modules_dir, module_name)
        is_modules = os.path.exists(os.path.join(module_base_path, "modules"))

        if not is_modules:
            return self.load_module(module_name, module_base_path)

        module_base_path = os.path.join(module_base_path, "modules")

        for current_module_name in os.listdir(module_base_path):
            if current_module_name == "__pycache__":
                continue
            if not os.path.isdir(os.path.join(module_base_path, current_module_name)):
                continue

            module_path = os.path.join(
                os.path.join(module_base_path, current_module_name), "module.py"
            )
            self.load_module(current_module_name, module_path)

    def unload_module(self, module_name: str) -> None:
        """
        Unloads a module by name.

        :param module_name: The name of the module to unload.
        """
        if module_name in self.modules:
            module = self.modules.pop(module_name)
            module.on_unload(self.client)

    def load_all_modules(self) -> None:
        """
        Loads all modules from the modules directory.
        """
        for folder_name in os.listdir(self.modules_dir):
            module_path = os.path.join(self.modules_dir, folder_name)
            if os.path.isdir(module_path):
                self.update_module(folder_name)
                self.load_modules(folder_name)
