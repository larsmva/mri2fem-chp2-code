
import logging
import argparse

from . import download_data
from . import subject_mesh
from . import create_mesh
from . import convert_to_dolfin_mesh
#from . import write_config

def setup_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Root parser
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Just print the command and do not run it",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print more information",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Download data parser
    download_parser = subparsers.add_parser("download", help="Download the dataset")
    download_data.add_arguments(download_parser)

    meshing_parser = subparsers.add_parser("mesh", help="Generates mesh from surface files.")
    create_mesh.add_arguments(meshing_parser)
    
    subject_mesh_parser =  subparsers.add_parser("subject-mesh", help="Generates mesh from surface files")
    subject_mesh.add_arguments(subject_mesh_parser)


    convert_mesh_parser = subparsers.add_parser("convert-mesh", help="Convert .mesh format to .h5")
    convert_to_dolfin_mesh.add_arguments(convert_mesh_parser)

    return parser


def dispatch(parser: argparse.ArgumentParser) -> int:
    args = vars(parser.parse_args())
    print( args)
    logging.basicConfig(level=logging.DEBUG if args.pop("verbose") else logging.INFO)

    logger = logging.getLogger(__name__)
    dry_run = args.pop("dry_run")
    command = args.pop("command")

    if dry_run:
        logger.info("Dry run: %s", command)
        logger.info("Arguments: %s", args)
        return 0

    try:
        if command == "download":
            download_data.main(**args)
        elif command == "mesh" : 
            create_mesh.main(**args)
        elif command == "subject-mesh": 
            subject_mesh.main(**args)
        elif command == "convert-format":
            convert_to_dolfin_mesh.main(**args)
        else:
            logger.error(f"Unknown command {command}")
            parser.print_help()
    except ValueError as e:
        logger.error(e)
        parser.print_help()

    return 0


def main() -> int:
    parser = setup_parser()

    return dispatch(parser)