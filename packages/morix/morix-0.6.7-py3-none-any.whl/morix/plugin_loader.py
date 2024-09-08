import os
import importlib.util
import logging
from .plugins.plugin_interface import PluginInterface
from .config_loader import config

logger = logging.getLogger(__name__)

class PluginLoader:
    def __init__(self):
        self.plugin_directory = config.plugins_path
        self.plugins = []

    def load_plugins(self):
        try:
            plugin_files = [f for f in os.listdir(self.plugin_directory) if f.endswith('.py') and f != '__init__.py']
        except FileNotFoundError:
            logger.debug(f"Plugin directory {self.plugin_directory} not found.")
            return
        for plugin_file in plugin_files:
            plugin_path = os.path.join(self.plugin_directory, plugin_file)
            module_name = os.path.splitext(plugin_file)[0]
            try:
                spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, PluginInterface) and attribute is not PluginInterface:
                        plugin_instance = attribute()
                        plugin_instance.initialize()
                        self.plugins.append(plugin_instance)
                        logger.info(f"Plugin {module_name} loaded and initialized.")
            except Exception as e:
                logger.error(f"Failed to load plugin {module_name}: {e}")

    def execute_plugin_function(self, function_name, args):
        results = [
            getattr(plugin, function_name)(**args)
            for plugin in self.plugins
            if hasattr(plugin, function_name)
        ]

        if not results:  # Если ни один плагин не имеет нужной функции
            logger.error(f"Plugin with function '{function_name}' not found")
            return None

        return results
