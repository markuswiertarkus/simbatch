
class Interaction:
    def __init__(self):
        pass
        
    def test(self):
        print "\n test Hou \n"
        
    # houdini executions     
    def houdini_open_scene(self, file):
        pass
        
    def houdini_import_ani(self, objects, dir):
        pass
        
    def houdini_import_cam(self, objects, file_or_dir):
        pass
        
    def houdini_import_obj(self, objects, file_or_dir):
        pass
    
    def houdini_simulate(self, ts, te, objects_names, cache_dir):
        pass   
        
    def houdini_render(self, ts, te, out_file=""):
        pass 
        
    def houdini_save_scene(self, file):
        pass
