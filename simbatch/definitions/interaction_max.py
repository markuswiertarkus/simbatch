
class Interaction:
    current_os = -1
    logger = None

    def __init__(self, current_os, logger):
        self.current_os = current_os
        self.logger = logger

    def print_info(self):
        self.logger.raw("This is interaction with 3dsmax")

    def max_open_scene(self, file):
        pass
        
    def max_import_ani(self, objects, dir):
        pass
        
    def max_import_cam(self, objects, file_or_dir):
        pass
        
    def max_import_obj(self, objects, file_or_dir):
        pass
    
    def max_simulate(self, ts, te, objects_names, cache_dir):
        pass   
        
    def max_render(self, ts, te, out_file=""):
        pass 
        
    def max_save_scene(self, file):
        pass
