import os
import re


class InOutStorage:
    batch = None
    comfun = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.p = batch.p
        self.s = batch.s

    @staticmethod
    def get_flat_name(name):
        return re.sub('\s', '_', name)

    def create_project_working_directory(self, directory):
        self.comfun.create_directory(directory)

    def create_schema_directory(self, directory):
        self.comfun.create_directory(directory)
        self.comfun.create_directory(directory + "base_setup\\")
        self.comfun.create_directory(directory + "computed_setups\\")
        self.comfun.create_directory(directory + "prevs\\")
        self.comfun.create_directory(directory + "cache\\")

    @staticmethod
    def get_path_from_full(full):
        return os.path.dirname(full)

    def get_files_from_dir(self, directory, types=""):
        files = []
        dir_path = self.get_path_from_full(directory)
        if os.path.isdir(dir_path):
            for fi in os.listdir(dir_path):
                if len(types) > 0:
                    if fi.endswith(types):
                        files.append(fi)
                else:
                    files.append(fi)
        return files

    def get_files_from_dir_by_object_names(self, directory, obj_list, file_type="", crowd_mode=False,
                                           crowd_mode_data=["pre", "post", 2, 10]):   # TODO  crowd_mode_data  as class
        files = []
        crowd = []
        zeros = []
        dir_path = directory   # TODO  check dir_path = self.get_path_from_full(dir)
        if os.path.isdir(dir_path):
            for fi in os.listdir(dir_path):
                if len(file_type) == 0:
                    file_name_to_check = fi.split(".")[0]
                else:
                    file_name_to_check = fi
                for o in obj_list:
                    if len(file_type) > 0:
                        o = o + "." + file_type
                    if o == file_name_to_check:
                        files.append(fi)
                        if crowd_mode:
                            crowd.append(o)
                            zeros.append("")
                    if crowd_mode:
                        o_name_pre = crowd_mode_data[0]
                        o_name_post = crowd_mode_data[1]
                        nr_zeros = crowd_mode_data[2]
                        for i in range(0, crowd_mode_data[3]):
                            nr_z = self.comfun.str_with_zeros(i, nr_zeros)
                            co = o_name_pre + nr_z + o_name_post
                            if len(file_type) > 0:
                                co = co + "." + file_type
                            if co == file_name_to_check:
                                files.append(fi)
                                crowd.append(co)
                                zeros.append(nr_z)
        return [files, crowd, zeros]

    def get_frame_range_from_dir(self, directory):    # TODO improve   for fi in os.listdir(dir):
        start = 0
        end = 0
        if os.path.isdir(directory):
            for fi in os.listdir(directory):
                if os.path.isfile(directory + "\\" + fi):
                    fi_no_ext = fi[:-4]
                    fi_arr = fi_no_ext.split("__")
                    if self.comfun.is_float(fi_arr[1]):
                        start = int(fi_arr[1])
                    if self.comfun.is_float(fi_arr[2]):
                        end = int(fi_arr[2])
            return [1, start, end]
        else:
            return [0, 0, 0]

    def generate_base_setup_file_name(self, schema_name="", ver=1):  # from existing TASK and SCHEMA data
        if len(self.p.projects_data) < self.p.current_project_index or self.p.current_project_index < 0:
            self.batch.logger.err(("Wrong current proj ID  ", self.p.current_project_index, len(self.p.projects_data)))
            return -1, ""
        else:
            proj_working_dir = self.p.current_project.working_directory_absolute
            schema_flat_name = self.get_flat_name(schema_name)
            directory = proj_working_dir + schema_flat_name + "\\base_setup\\"
            file_version = "_v" + self.comfun.str_with_zeros(ver, self.p.current_project.zeros_in_version)
            # file_ext = self.batch.d.get_base_setup_ext(self.s.runtime_env)
            file_ext = "TODO12"
            return 1, directory + schema_flat_name + file_version + file_ext

    #  get directory pattern for current project
    #  pattern is generated basis on directories structure on storage
    #  used for construct new path, generate path for load
    def get_dir_patterns(self, directory):
        self.batch.logger.db(("(get_dir_patterns) deep debug start dir:", directory))
        full_dir_pattern = None
        return full_dir_pattern
