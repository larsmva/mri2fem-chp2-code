import argparse
import typing

from . import (
    create_mesh,
    repair_surface,
    sequential_union,
    make_cisterna_magna,
    get_foramen_magnum,

)

__all__ = [
    "add_svmtk_parser",
    "dispatch",
    "surface_to_mesh",
    "create_mesh",
    "repair_surface"
    "sequential_union" 
    "make_cisterna_magna",
    "get_foramen_magnum",
]


def add_svmtk_parser(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="svmtk-command")

    # Create mesh parser
    create_mesh_parser = subparsers.add_parser("create-mesh", help="create a mesh")
    create_mesh.add_arguments(create_mesh_parser)

    # Repair surface parser
    repair_surface_parser = subparsers.add_parser("repair-surface", help="Repair a surface")
    repair_surface.add_arguments(repair_surface_parser)

    sequential_union_parser = subparsers.add_parser("sequential-union", help="Takes the union of three surfaces sequentially.")
    sequential_union.add_arguments(sequential_union_parser)
 
    make_cisterna_magna_parser = subparsers.add_parser("make-cisterna-magna", help="Smooth a surface")
    make_cisterna_magna.add_arguments(make_cisterna_magna_parser)
    
    get_foramen_magnum_parser = subparsers.add_parser("get-foramen-magnum", help="Smooth a surface")
    get_foramen_magnum.add_arguments(get_foramen_magnum_parser)            

def dispatch(command, args: dict[str, typing.Any]) -> int:

    if command == "create-surface":
        create_surface.main(**args)

    elif command == "repair-surface":
        repair_surface.main(**args)

    elif command == "sequential-union":
        sequential_union.main(**args)

    elif command == "make-cisterna-magna":
        make_cisterna_magna.main(**args)

    elif command == "get-foramen-magnum":
       get_foramen_magnum.main(**args)

    else:
        raise ValueError(f"Unknown command {command}")

    return 0
