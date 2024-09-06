from blue_objects import NAME, VERSION, DESCRIPTION, ICON
from blue_objects.logger import logger
from blueness.argparse.generic import main

main(
    ICON=ICON,
    NAME=NAME,
    DESCRIPTION=DESCRIPTION,
    VERSION=VERSION,
    main_filename=__file__,
    logger=logger,
)
