from maya import cmds
import math


def build_turntable(load_file=None):
    if load_file:
        # Open the file
        loaded = cmds.file(load_file, r=True)
        # Select and group the set
        cmds.select(ado=True)
        cmds.group(n='Set_prep')
        # Get the set/scene size from the bounding box
        cmds.select('Set_prep')
        scene_bb = cmds.xform(q=True, bb=True)
        # Find the center from the bounding box
        x_center = scene_bb[3] - ((scene_bb[3] - scene_bb[0])/2)
        y_center = scene_bb[4] - ((scene_bb[4] - scene_bb[1])/2)
        z_center = scene_bb[5] - ((scene_bb[5] - scene_bb[2])/2)
        bb_center = [x_center, y_center, z_center]
        # calculate a new height for the camera based on the bounding box
        cam_height = scene_bb[4] - scene_bb[1]
        # Create a new camera and fit it to the current view
        cam = cmds.camera(n='turn_table_cam')
        cmds.lookThru(cam)
        cmds.viewFit()
        # Get the position of the new camera after placement
        cam_pos = cmds.xform(q=True, ws=True, t=True)
        # Separate out the mins and maxs of the bounding box for triangulation
        x_min = scene_bb[0]
        x_max = scene_bb[3]
        y_min = scene_bb[1]
        y_max = scene_bb[4]
        z_min = scene_bb[2]
        z_max = scene_bb[5]
        # Get the cube root hypotenuse of the bounding box to calculate the overall scene's widest distance
        cube_diff = math.pow((x_max - x_min), 3) + math.pow((y_max - y_min), 3) + math.pow((z_max - z_min), 3)
        max_hypotenuse = cube_diff ** (1./3.)
        # Cut the width in half to create a 90 degree angle
        half_width = max_hypotenuse/2
        # Get the horizontal aperture. Only the inch aperture is accessible, so mm aperture and field of view must be calculated from that
        horizontalApertureInch = cmds.getAttr('%s.horizontalFilmAperture' % cam[1])
        # convert to mm
        horizontalAperture_mm = 2.54 * horizontalApertureInch * 10
        # Get focal length
        focalLength = cmds.getAttr('%s.focalLength' % cam[1])
        # Calculate FOV from horizontal aperture and focal length
        fov = math.degrees(2 * math.atan(horizontalAperture_mm/(focalLength * 2)))
        # Cut the FOV in half to get angle of right angle.
        half_angle = fov/2
        # Calculate the distance for the camera
        angle_tan = math.tan(half_angle)
        distance = cam_pos[2] - (half_width/angle_tan)
        # Set the new camera distance and height
        cmds.setAttr('%s.ty' % cam[0], cam_height)
        cmds.setAttr('%s.tz' % cam[0], distance)
        # Get the new camera position        
        cam_pos = cmds.xform(q=True, t=True, ws=True)
        # Calculate the decension angle from the center of the scene to the new camera position
        cam_height = cam_pos[1] - bb_center[1]
        cam_dist = cam_pos[2] - bb_center[2]
        cam_angle = -1 * (math.degrees(cam_height/cam_dist))
        # Set the declination angle
        cmds.setAttr('%s.rx' % cam[0], cam_angle)
        # Group the camera, center the pivot, and animate the rotation
        cmds.group(n='turn_table_rotate')
        cmds.xform(piv=[x_center, y_center, z_center])
        cmds.setKeyframe('turn_table_rotate.ry', v=0.0, ott='linear', t=1)
        cmds.setKeyframe('turn_table_rotate.ry', v=360.0, itt='linear', t=120)


def setup_scene(bb=None):
    if bb:
        pass
        
    
if __name__ == '__main__':
    build_turntable(load_file='C:/Users/sleep/OneDrive/Documents/3D/lazy_suzanne/scenes/test_junk.mb')
    # build_turntable(load_file='C:/Users/sleep/OneDrive/Documents/3D/character_builder/scenes/character_builder_test_v04.mb')
    # build_turntable(load_file='C:/Users/sleep/OneDrive/Documents/3D/lazy_suzanne/scenes/turntable_test_v003.mb')