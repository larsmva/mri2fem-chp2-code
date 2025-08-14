
def repair_surface(surface, edge_length=1.0):
    # Keeps the largest connected component.
    surface.keep_largest_connected_component() 
    # Fills most holes in triangulation, not topological.
    surface.fill_holes()
    # Remeshing surface to specified edge length
    surface.isotropic_remeshing(edge_length, 5, False)
    # Volume perserving surface smoothing.
    surface.smooth_taubin(20)     
    # Separate narrow gaps to avoid bridges in meshing.
    print("Narrow gaps: ",surface.separate_narrow_gaps(.4,.4,200)) 
     # Removes self-intersection       
    surface.repair_self_intersections(volume_threshold=0.4,
                                      cap_threshold=170,
                                      needle_threshold=1.5,
                                      collapse_threshold=0.4)   
    return surface

def sequential_union(white, brainstem, cerebellum):
    # Union between brainstem and cerebellum surfaces
    brainstem.union(cerebellum)
    # Repair any faults in the new surface.
    brainstem = repair_surface(brainstem)
    # Union between white and brainstem surfaces.
    white.union(brainstem)
    # Repair any faults in the new surface
    white = repair_surface(white)
    return white

def make_cisterna_magna(ventricles, white, radius=2.0, edge_length=1.0):
    # Computes the centerlines as a list of polylines. 
    # z-axis indicates sorted with low to high z-coordinates. 
    centerlines = ventricles.mean_curvature_flow("z-axis")
    # The lowest z-coordinate.
    p1 = centerlines[0][0] 
    # Find the closest point on the white surface. 
    p2 = white.get_closest_points(p1)[0]
    # Extend the point in the same direction.
    p2 = p2 + 2 * svm.Vector_3(p1, p2)
    # Construct an empty Surface.
    cisterna_magna = svm.Surface()
    # Construct a cylinder with a specified radius.
    cisterna_magna.make_cylinder(p1, p2, radius, edge_length)
    return cisterna_magna

def get_foramen_magnum(brainstem, z0, radius=20):
    # Define a Plane object at z = z0
    zplane = svm.Plane_3(0,0,1,-z0)
    # Get perpendicular cut where the plane intersect the centerline 
    surf = brainstem.get_perpendicular_cut(zplane, radius) 
    return surf

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
    parser.add_argument('--rhpial'    , default=envpath+"rhpial.stl", type=str)
    parser.add_argument('--lhpial'    , default=envpath+"lhpial.stl", type=str)
    parser.add_argument('--lhwhite'   , default=envpath+"lhwhite.stl", type=str)
    parser.add_argument('--rhwhite'   , default=envpath+"rhwhite.stl", type=str)
    parser.add_argument('--brainstem' , default=envpath+"brainstem.stl", type=str)
    parser.add_argument('--cerebellum', default=envpath+"cerebellum.stl", type=str)
    parser.add_argument('--dura'      , default=envpath+"dura.stl", type=str)
    parser.add_argument('--ventricles', default=envpath+"ventricles.stl", type=str)
    
    parser.add_argument('--edge_length', type=float)
    parser.add_argument('--out', type=str, default="gonzo.mesh")
  
    start_time = time.time()        
    Z = parser.parse_args()
    # ----- Load surfaces -----    
    # Load and repair the cerebellum surface
    cerebellum = svm.Surface(Z.cerebellum)
    cerebellum = repair_surface(cerebellum)
    # Load and repair the brainstem surface
    brainstem = svm.Surface(Z.brainstem)
    brainstem = repair_surface(brainstem)
    # Load and repair the bounding surface
    dura = svm.Surface(Z.dura)
    dura = repair_surface(dura)
    # Load and repair the right hemisphere pial surface.
    rhpial = svm.Surface(Z.rhpial)
    rhpial = repair_surface(rhpial)
    # Load and repair the left hemisphere pial surface.
    lhpial = svm.Surface(Z.lhpial)
    lhpial = repair_surface(lhpial)

    # Load and repair the left hemisphere white surface.
    lhwhite = svm.Surface(Z.lhwhite)
    lhwhite = repair_surface(lhwhite)

    # Load and repair the right hemisphere white surface.
    rhwhite = svm.Surface(Z.rhwhite)
    rhwhite = repair_surface(rhwhite)

    # Load and repair the surface of the ventricle system
    ventricles = svm.Surface(Z.ventricles)
    ventricles = repair_surface(ventricles)

    # ----- Merge white surfaces -----
    # White surfaces only partially overlapping due to smoothing effects
    white = svm.union_partially_overlapping_surfaces(rhwhite, lhwhite)

    # Repair surface, as the union may result in self-intersections.
    white = repair_surface(white)

    # ----- Separete pial surfaces ------
    # Separate overlapp between the pial surfaces.
    svm.separate_overlapping_surfaces(rhpial, lhpial, white)
    # Separate the pial surfaces.
    svm.separate_close_surfaces(rhpial, lhpial, white)
    
    # ----- Define foramen magnum plane -----
    # Foramen magnum set 10 mm lower than the cerebellum surface
    z0 = cerebellum.span(2)[0] - 10
    # Creates a surface object close to the foramen magnum
    foramen_magnum = get_foramen_magnum(brainstem, z0)

    # ----- Making surfaces anatomical correct -----
    # Adjust cerebellum to be disjointed from the pial surfaces
    svm.expose(cerebellum,lhpial)
    svm.expose(cerebellum,rhpial)
    # Adjust dura to enclose the cerebellum surface    
    svm.enclose(dura,cerebellum)
    # Merge surfaces brainstem,cerebellum and white.
    white = sequential_union(white, brainstem, cerebellum)
    # surface.cut_perpenticular( point ) 
    # svm.make_connection()
    # Adjust white to enclose the ventricular surface 
    # Union with ventricles.
    white.union(ventricles)
    # Repair any faults in the new surface
    white = repair_surface(white)
    # Expand white surface to enclose the ventricles
    svm.enclose(white,ventricles)
    # Contract ventricle surface to inside the white
    svm.embed(ventricles,white)
    # Create cisterna magna 
    cisterna_magna = make_cisterna_magna(ventricles, white)   
    # Subtract the cisterna magna from the white surface
    white.difference(cisterna_magna)
    # Repair any faults in the new surface
    white = repair_surface(white)
    # Adjust dura/bounding surface to enclose the pial surfaces
    svm.enclose(dura,lhpial)
    svm.enclose(dura,rhpial)


    foramen_magnum.save("final-fm.stl")
    lhpial.save("final-lhpial.stl") 
    rhpial.save("final-rhpial.stl")       
    white.save("final-white.stl") 
    ventricles.save("final-ventricles.stl") 
    dura.save("final-dura.stl")

 
    # Clip the bounding and white surface.
    dura.clip(foramen_magnum, invert=True)
    white.clip(foramen_magnum, invert=True)
     
    # Set the structure of the surfaces.
    surfaces = [dura,lhpial,rhpial,white,ventricles]

    # ----- Defining the SubdomainMap -----
    # Sets the subdomain tags based on 
    smap = svm.SubdomainMap(len(surfaces))
    
    smap.add("10000", 1)
    smap.add("11000", 2)
    smap.add("10100", 2)
    smap.add("*10", 3)
    smap.add("*1", 4)

    # Create domain object used for meshing
    domain = svm.Domain(surfaces, smap)

    # ----- Preserve sharp edges -----
    # Detect and preserve sharp edges in a given plane.
    domain.add_sharp_border_edges(white, foramen_magnum, 60)
    # Detect and preserve sharp edges in a given plane.
    domain.add_sharp_border_edges(dura, foramen_magnum,60)    
    # Create mesh with mesh resolution set to 64
    domain.create_mesh(64)

    # ----- Mesh optimiztion -----   
    # Perform silver perturbation
    domain.perturb()    
    # Perform exude silvers 
    domain.exude()
    # Run surface segmentation on the interface (1,0) 
    domain.boundary_segmentations((1, 0), 60)
    # Save mesh to file.
    domain.save(envpath+Z.out)
