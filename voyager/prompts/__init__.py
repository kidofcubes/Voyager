# import pkg_resources
from importlib.resources import files
import voyager.utils as U


def load_prompt(prompt):
    # package_path = pkg_resources.resource_filename("voyager", "")
    package_path = files("voyager")
    return U.load_text(f"{package_path}/prompts/{prompt}.txt")
