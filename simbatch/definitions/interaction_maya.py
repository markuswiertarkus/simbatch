class Interaction:
    def __init__(self):
        pass
        
    def test(self):
        print "\n interaction test maya \n"
    
    # maya executions
    
    def save_current_scene_as(self, file):
        print "TODO: interaction save as"
    
    def maya_open_scene(self, file):
        print "TODO: maya_open_scene"
        pass
        
    def maya_get_selection(self):
        print "TODO: maya_get_selection"
        return "test sel obj"
        
    def maya_get_camera(self):
        print "TODO: maya_get_camera"
        pass
        
    def maya_import_ani(self, objects, dir):
        pass
        
    def maya_import_cam(self, objects, file_or_dir):
        pass
        
    def maya_import_obj(self, objects, file_or_dir):
        pass
        
    def maya_set_param(self, object, property, value):
        pass
        
    def maya_simulate_ncloth(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_nhair(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_nparticle(self, ts, te, objects_names, cache_dir):
        pass
        
    def maya_simulate_fume(self, ts, te, fume_container, cache_dir):
        pass
        
    def maya_simulate_fumewt(self, ts, te, fume_container, cache_dir):
        pass
        
    def maya_render_blast(self, ts, te, out_file=""):
        pass
        
    def maya_render_software(self, ts, te, out_file=""):
        pass
        
    def maya_save_scene(self, file):
        pass
        
    def maya_script_py(self, file):
        pass
        
    def maya_script_mel(self, file):
        pass 

    def maya_get_scene_objects(self):
        print "\n test maya_get_scene_objects\n"
