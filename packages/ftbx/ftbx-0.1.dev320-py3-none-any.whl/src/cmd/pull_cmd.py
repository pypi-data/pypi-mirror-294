"""

    PROJECT: flex_toolbox
    FILENAME: pull_cmd.py
    AUTHOR: David NAISSE
    DATE: August 5th, 2024

    DESCRIPTION: pull command functions
"""

import logging
import os

from rich.logging import RichHandler
from src._environment import Environment
from src._objects import ObjectType, Objects, SubItems
from src.utils import FTBX_LOG_LEVELS, convert_to_native_type

# logger
logging.basicConfig(
    level=FTBX_LOG_LEVELS.get(os.getenv("FTBX_LOG_LEVEL", "INFO").upper()),
    format="%(name)s | %(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


def pull_command_func(**kwargs) -> bool:
    """
    Action on pull command.
    """

    logger.debug(f"Entering {__name__} with args: {kwargs}. ")

    # add exactNameMatch=true when name is provided
    if kwargs["filters"]:
        if any("name=" in f for f in kwargs["filters"]) and not any(
            "fql" in f for f in kwargs["filters"]
        ):
            kwargs["filters"].append("exactNameMatch=true")

    # multi-envs
    for env in kwargs["from_"]:
        environment = Environment.from_env_file(environment=env)

        # for pull all
        if kwargs["object_type"] == "all":
            for object_type in ObjectType:
                objects = Objects(
                    object_type=object_type,
                    sub_items=SubItems.from_object_type(object_type=object_type),
                    filters={},
                    post_filters=[],
                    mode="full",
                    with_dependencies=False,
                    save_results=True,
                )

                # no instances (assets, jobs, events...)
                if not objects.is_instance:
                    objects.get_from(environment=environment)
        else:
            # get objects
            object_type = ObjectType.from_string(string=kwargs["object_type"])
            objects = Objects(
                object_type=object_type,
                sub_items=SubItems.from_object_type(object_type=object_type),
                filters=(
                    {
                        filter.split("=")[0]: convert_to_native_type(
                            filter.split("=")[1]
                        )
                        for filter in kwargs["filters"]
                    }
                    if kwargs["filters"]
                    else {}
                ),
                post_filters=kwargs['post_filters'] if kwargs['post_filters'] else [],
                mode="full",
                with_dependencies=kwargs['with_dependencies'],
                save_results=True,
            )
            objects.get_from(environment=environment)

    return True
