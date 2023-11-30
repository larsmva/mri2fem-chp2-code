
def repair_surface(surface, edge_length=1.0):
    # Keeps the largest connected component.
    surface.keep_largest_connected_component() 
    # Fills most holes in triagnulation, not topological.
    surface.fill_holes()
    # Volume preserving surface smoothing.
    surface.smooth_taubin(20) 
    # Removes self-intersection.  
    surface.repair_self_intersections()   
    # Remeshing surface to specified edge length
    surface.isotropic_remeshing(edge_length, 5, False)
    # Separate narrow gaps to avoid bridges in meshing.
    surface.separate_narrow_gaps()
    return surface





def sequential_union_wm_bs_c(white, brainstem, cerebellum):
    # Union between brainstem and cerebellum surfaces
    brainstem.union(cerebellum)
    # Repair any faults in the new surface.
    brainstem = repair_surface(brainstem)
    # Union between white and brainstem surfaces.
    white.union(brainstem)
    # Repair any faults in the new surface
    white = repair_surface(white)
    return white


def enclose_pial(bounding_surface, rhpial, lhpial):
    # Expands bounding surface to enclose the pial surfaces    
    bounding_surface.enclose(lhpial)
    bounding_surface.enclose(rhpial)
    # Separate the pial and bounding surfaces
    bounding_surface.separate(lhpial)
    bounding_surface.separate(rhpial)
    return bounding_surface


def fix_cerebellum(cerebellum, lhpial, rhpial, bounding_surface):
    # Moves cerebellum outside the pial surfaces.
    cerebellum.expose(lhpial); cerebellum.expose(rhpial)
    # Moves cerebellum inside the bounding surface.
    cerebellum.embed(bounding_surface)
    # Separate cerebellum from the bounding surface.
    cerebellum.separate(bounding_surface)
    return cerebellum


def enclose_ventricles(white, ventricles):
    # Union with ventricles.
    white.union(ventricles)
    # Repair any faults in the new surface
    white = repair_surface(white)
    # Expand white surface to enclose the ventricles
    white.enclose(ventricles)
    # Contract ventricle surface to inside the white
    ventricles.embed(white)
    # Separate white and ventricle surface
    white.separate(ventricles)
    return white, ventricles


def make_cisterna_magna(ventricles, white, radius=2.0):
    # Computes the centerlines as a list of polylines.
    centerlines = ventricles.mean_curvature_flow()
    # Finds the point with the lowest z-coordinate.
    p1 = find_lowest_point(centerlines)
    # Find the closest point on the white surface.
    p2 = white.get_closest_points(p1, 1)[0]
    # Extend the point in the same direction.
    p2 = p2 + 2 * svm.Vector_3(p1, p2)
    # Construct an empty Surface.
    cisterna_magna = svm.Surface()
    # Construct a cylinder with a specified radius.
    cisterna_magna.make_cylinder(p1, p2, radius, 1.0)
    return cisterna_magna


def get_foramen_magnum(brainstem, z0):
    # Computes and returns centerlines as 2D array
    centerlines = brainstem.mean_curvature_flow()
    # Set default values
    num = 0; min_index = 0; min_value = 0
    # Finds the centerline with a point closest to z0.
    for no, points in enumerate(centerlines):
        index, value = min(enumerate(points),
                           key=lambda i: abs(i[1].z()-z0))
        if abs(z0 - value.z()) < abs(z0 - min_value):
            min_value = value.z(); num = no; min_index = index
    # Define centerline with a point closest to z0
    centerline = centerlines[num]
    # Define point closest to z0
    point = centerline[min_index]
    # Sets the orientation of the normal vector downwards
    if centerline[min_index+5].z() < centerline[min_index-5].z():
        vector = svm.Vector_3(point, centerline[min_index+10])
    else:
        vector = svm.Vector_3(point, centerline[min_index-10])
    # Create a Plane given a point and normal vector
    return svm.Plane_3(point, vector)


def find_lowest_point(centerlines):
    # Set default values
    num = 0; min_index = 0; min_value = 0
    # Find the centerline and point with the loweste z coordinate
    for no, points in enumerate(centerlines):
        index, value = min(enumerate(points),
                           key=lambda i: i[1].z())
        if abs(z0 - value.z()) < abs(z0 - min_value):
            min_value = value.z(); num = no; min_index = index
    return centerlines[num][min_index]


if __name__ == '__main__':

    import SVMTK as svm
    import argparse
    import time 
    parser = argparse.ArgumentParser()
    parser.add_argument('--rhpial', default="rhpial.stl", type=str)
    parser.add_argument('--lhpial', default="lhpial.stl", type=str)
    parser.add_argument('--lhwhite', default="lhwhite.stl", type=str)
    parser.add_argument('--rhwhite', default="rhwhite.stl", type=str)
    parser.add_argument('--brainstem', default="brainstem.stl", type=str)
    parser.add_argument('--cerebellum', default="cerebellum.stl", type=str)
    parser.add_argument('--dura', default="dura.stl", type=str)
    parser.add_argument('--ventricles', default="ventricles.stl", type=str)
    parser.add_argument('--edge_length', type=float)
    parser.add_argument('--out', type=str, default="Bernie.mesh")
  
    start_time = time.time()        
    Z = parser.parse_args()
    # Load and repair the cerebellum surface
    cerebellum = svm.Surface(Z.cerebellum)
    cerebellum = repair_surface(cerebellum)
  
    # Load and repair the brainstem surface
    brainstem = svm.Surface(Z.brainstem)
    brainstem = repair_surface(brainstem)

    # Load and repair the bounding surface
    bounding_surface = svm.Surface(Z.dura)
    bounding_surface = repair_surface(bounding_surface)

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
    white = svm.union_partially_overlapping_surfaces(rhwhite, lhwhite, 50.0, 1.0 ,.2)

    # Repair surface, as the union may result in self-intersections.
    white = repair_surface(white)

    # ----- Separete pial surfaces ------
    # Separate overlapp between the pial surfaces.
    svm.separate_overlapping_surfaces(rhpial, lhpial, white,-1.0,0.2)
    # Separate the pial surfaces.
    svm.separate_close_surfaces(rhpial, lhpial, white,-1.0,0.1)
    # Separate narrow folds in the pial surfaces.
    rhpial.separate_narrow_gaps()
    lhpial.separate_narrow_gaps()
    
    # ----- Define foramen magnum plane -----
    # Foramen magnum set 10 mm lower than the cerebellum surface
    z0 = cerebellum.span(2)[0] - 10
    # Creates a Plane object close to the foramen magnum
    foramen_magnum = get_foramen_magnum(brainstem, z0)
    # Adjust cerebellum so that it is anatomical correct
    fix_cerebellum(cerebellum, lhpial, rhpial, bounding_surface)     

    # Merge surfaces brainstem,cerebellum and white.
    white = sequential_union(white, brainstem, cerebellum)

    # Adjust white so that it is anatomical correct.
    white, ventiricles = enclose_ventricles(white, ventricles)
    # Creates a cylinder
    cisterna_magna = make_cisterna_magna(ventricles, white)
   
    # Subtract the cisterna magna from the white surface
    white.difference(cisterna_magna)
    # Repair any faults in the new surface
    white = repair_surface(white)
    # Adjust bounding surface so that it is anatomical correct.
    bounding_surface = enclose_pial(bounding_surface,rhpial,lhpial)

    # Clips the bounding and white surface.
    bounding_surface.clip(foramen_magnum,True)
    white.clip(foramen_magnum,True)
     
    # Set the structure of the surfaces.
    surfaces = [bounding_surface,lhpial,rhpial,white,ventricles]
    # ----- Defining the SubdomainMap -----
    # Sets the subdomain tags based on 

    smap = svm.SubdomainMap(len(surfaces))
    smap.add("10000", 1)
    smap.add("*10", 2)
    smap.add("11000", 3)
    smap.add("10100", 3)
    smap.add("*1", 4)

    # Sets the interface tag between subdomains.
    smap.add_interface((2, 0), 2)
    smap.add_interface((2, 1), 3)
    smap.add_interface((3, 1), 4)
    smap.add_interface((3, 2), 5)
    smap.add_interface((4, 1), 6)
    smap.add_interface((4, 2), 7)
    smap.add_interface((5, 0), 8)
    smap.add_interface((6, 0), 9)

    # Domain object
    domain = svm.Domain(surfaces, smap)

    # ----- Preserve sharp edges -----
    # Detect and preserve sharp edges in a given plane.
    domain.add_sharp_border_edges(white, foramen_magnum, 60)
    # Detect and preserve sharp edges in a given plane.
    domain.add_sharp_border_edges(bounding_surface,foramen_magnum,60)    
    # Create mesh
    domain.create_mesh(64)

    # ----- Mesh optimiztion -----   
    # Perform silver perturbation
    domain.perturb()    
    # Perform exude silvers 
    domain.exude()
    # Run surface segmentation on the interface (1,0)
    domain.boundary_segmentations((1, 0), 60)
    # Save mesh to file.
    domain.save("Subject.mesh")
