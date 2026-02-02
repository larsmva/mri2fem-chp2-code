
from pathlib import Path
import SVMTK as svm

from . import create_mesh

def add_arguments(parser ):
    parser.add_argument('-s','--subject'    , default=f"", type=str,      help="The FreeSurfer subject folder." ) 
    parser.add_argument('-o','--output'    , default=f"", type=str,      help="The mesh output" ) 
    parser.add_argument('--edge_length', default=1.0, type=float,  help="Target surface edge length duirng remeshing (Default=1.0) ")
    parser.add_argument('--resolution', default=64,type=float,  help="The mesh resolution of the mesh. The bounding radius of all surfaces divided by the resolution gives targt cell_size. ")
    parser.add_argument('--export_fenicsx', action='store_true', help =" Option to export the mesh to npz format compatible with FEniCSx.")
 

def main( subject, edge_length, resolution, output, export_fenicsx ):
    create_mesh.main(f"{subject}/output/rhpial.stl", 
         f"{subject}/output/lhpial.stl",
         f"{subject}/output/lhwhite.stl",
         f"{subject}/output/rhwhite.stl",
         f"{subject}/output/brainstem.stl",
         f"{subject}/output/cerebellum.stl",
         f"{subject}/output/dura.stl",
         f"{subject}/output/ventricles.stl",
         edge_length,
         resolution,
         output, 
         export_fenicsx)



    
if __name__ == '__main__':

    import SVMTK as svm
    import argparse
    import time 
    
    import os

    if os.environ.get("MRI2FEMIIDATA") !=None :
       envpath = os.environ.get("SUBJECT")+"/output/"
    else :
       envpath = ""
 

    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--subject', default=envpath+"ventricles.stl", type=str)
    parser.add_argument('--export_fenicsx', action='store_true')
    parser.add_argument('--resolution', type=float, default=64)
    parser.add_argument('--edge_length', type=float, default=1.0)
    parser.add_argument('-o','--output', type=str, default=envpath+"gonzo.mesh")
    Z = parser.parse_args()
    
    create_mesh.main(f"{Z.subject}/output/rhpial.stl", 
         f"{Z.subject}/output/lhpial.stl",
         f"{Z.subject}/output/lhwhite.stl",
         f"{Z.subject}/output/rhwhite.stl",
         f"{Z.subject}/output/brainstem.stl",
         f"{Z.subject}/output/cerebellum.stl",
         f"{Z.subject}/output/dura.stl",
         f"{Z.subject}/output/ventricles.stl",
         Z.edge_length,
         Z.resolution,
         Z.output, 
         Z.export_fenicsx)
