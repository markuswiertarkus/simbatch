import os
import re


class PredefinedVariables:
    batch = None

    predefined = {
        "schema_base_setup": {"type": "f", "function": "get_schema_base_setup"},
        "shot_cache_dir": {"type": "d", "function": "get_shot_cache_dir"},
        "shot_cam_dir": {"type": "d", "function": "get_shot_cam_dir"},
        "project_props_dir": {"type": "d", "function": "get_project_props_dir"},
        "shot_camera_file": {"type": "f", "function": "get_shot_camera_file"},
        "shot_prev_file": {"type": "f", "function": "get_shot_prev_file"},
        "shot_simed_setup": {"type": "f", "function": "get_shot_simed_setup"},
        "scripts_dir": {"type": "d", "function": "get_scripts_dir"}
    }
    defaults = {
        "sim_ts": "get_sim_time_start",
        "sim_te": "get_sim_time_end",
        "prev_ts": "get_prev_time_start",
        "prev_te": "get_prev_time_end",
        "d": "get_working_directory",
        "f": "get_default_file",
        "o": "get_default_object",
        "p": "get_default_param",
        "v": "get_default_value"
    }

    def __init__(self, batch):
        self.batch = batch

    # convert predefined variable into final value
    def convert_var_to_val(self, var, template):
        #  TODO multi val in var
        if var in self.predefined:
            function_to_eval = "self." + self.predefined[var]["function"] + "()"
            try:
                eval_ret = eval(function_to_eval)
                return template.replace("<"+self.predefined[var]["type"]+">", eval_ret)
            except ValueError:
                # TODO ex
                return None
        else:
            return None

    def convert_undefined_to_default(self, template):
        # TODO optimize !
        # for de in self.defaults:
        for key, get_default in self.defaults.items():
            check = "<"+key+">"
            if template.find(check) > 0:
                # print "check", check ,  "   get_default: " , get_default
                try:
                    function_to_eval = "self." + get_default + "()"
                    eval_ret = eval(function_to_eval)
                    # print "eval_ret", eval_ret
                    template = template.replace(check, str(eval_ret))
                except ValueError:
                    # TODO ex
                    pass
        return template

    def get_schema_base_setup(self):
        ret = self.batch.sio.generate_base_setup_file_name()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_cache_dir(self):
        ret = self.batch.sio.generate_shot_cache_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_cam_dir(self):
        ret = self.batch.sio.generate_shot_cam_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_camera_file(self):
        ret = self.batch.sio.generate_shot_camera_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_prev_file(self):
        ret = self.batch.sio.generate_shot_prev_file()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_project_props_path(self):
        ret = self.batch.sio.generate_project_props_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_shot_simed_setup(self):
        ret = self.batch.sio.generate_shot_simed_setup()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_scripts_path(self):
        ret = self.batch.sio.generate_scripts_path()
        if ret[0] > 0:
            return ret[1]
        else:
            return ""

    def get_sim_time_start(self):
        return self.batch.tsk.current_task.sim_frame_start

    def get_sim_time_end(self):
        return self.batch.tsk.current_task.sim_frame_end

    def get_prev_time_start(self):
        return self.batch.tsk.current_task.prev_frame_start

    def get_prev_time_end(self):
        return self.batch.tsk.current_task.prev_frame_end

    def get_working_directory(self):
        ret = self.batch.prj.current_project.working_directory_absolute
        if ret is not None:
            return ret
        else:
            return ""

    def get_default_file(self):
        return "[default_file]"

    def get_default_object(self):
        return "[default_object]"

    def get_default_param(self):
        return "[default_param]"

    def get_default_value(self):
        return "[default_value]"


class StorageInOut:
    batch = None
    comfun = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.prj = batch.prj
        self.sts = batch.sts
        self.predefined = PredefinedVariables(batch)
        self.dir_separator = batch.sts.dir_separator

    @staticmethod
    def get_flat_name(name):
        return re.sub('\s', '_', name)

    def create_project_working_directory(self, directory):
        self.comfun.create_directory(directory)

    def create_schema_directory(self, directory):
        self.comfun.create_directory(directory + "base_setup" + self.sts.dir_separator)
        self.comfun.create_directory(directory + "computed_setups" + self.sts.dir_separator)
        self.comfun.create_directory(directory + "prevs" + self.sts.dir_separator)
        self.comfun.create_directory(directory + "cache" + self.sts.dir_separator)

    def get_files_from_dir(self, directory, types=""):
        files = []
        dir_path = self.comfun.get_path_from_full(directory)
        if os.path.isdir(dir_path):
            for fi in os.listdir(dir_path):
                if len(types) > 0:
                    if fi.endswith(types):
                        files.append(fi)
                else:
                    files.append(fi)
        return files

    def get_files_from_dir_by_object_names(self, directory, obj_list, file_type="", crowd_mode=False,
                                           crowd_mode_data=("pre", "post", 2, 10)):   # TODO  crowd_mode_data  as class
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
                if os.path.isfile(directory + self.sts.dir_separator + fi):
                    fi_no_ext = fi[:-4]
                    fi_arr = fi_no_ext.split("__")
                    if self.comfun.is_float(fi_arr[1]):
                        start = int(fi_arr[1])
                    if self.comfun.is_float(fi_arr[2]):
                        end = int(fi_arr[2])
            return [1, start, end]
        else:
            return [0, 0, 0]

    def generate_base_setup_file_name(self, schema_name="", ver=0):  # from existing TASK and SCHEMA data
        if len(self.prj.projects_data) < self.prj.current_project_index or self.prj.current_project_index < 0:
            self.batch.logger.err(("Wrong current proj ID  ", self.prj.current_project_index,
                                   len(self.prj.projects_data)))
            return -1, ""
        else:
            if len(schema_name) == 0:
                if self.batch.sch.current_schema is not None:
                    schema_name = self.batch.sch.current_schema.schema_name
                    if ver == 0:
                        ver = self.batch.sch.current_schema.schema_version
                else:
                    self.batch.logger.err("generate_base_setup_file_name from schema: None")
                    return -1, ""

            proj_working_dir = self.prj.current_project.working_directory_absolute
            schema_flat_name = self.get_flat_name(schema_name)
            directory = proj_working_dir+schema_flat_name+self.dir_separator+"base_setup"+self.dir_separator
            file_version = "_v" + self.comfun.str_with_zeros(ver, self.prj.current_project.zeros_in_version)
            file_ext = self.batch.dfn.get_current_setup_ext()
            return 1, directory + schema_flat_name + file_version + "." + file_ext

    def generate_shot_dir(self):
        if self.prj.current_project is None or \
                self.batch.sch.current_schema is None or \
                self.batch.tsk.current_task is None:
            return -1, ""
        else:
            shot_dir = self.prj.current_project.working_directory_absolute
            schema_name = self.batch.sch.current_schema.schema_name
            shot_dir += self.get_flat_name(schema_name) + self.dir_separator
            cur_tsk = self.batch.tsk.current_task
            if len(cur_tsk.sequence) > 0:
                shot_dir += cur_tsk.sequence + self.dir_separator
            if len(cur_tsk.shot) > 0:
                shot_dir += cur_tsk.shot + self.dir_separator
            if len(cur_tsk.take) > 0:
                shot_dir += cur_tsk.take + self.dir_separator

            return 1, shot_dir

    def generate_shot_simed_setup(self, ver=0):
        ret = self.generate_shot_dir()
        if ret[0] == 1:
            ret_file_and_path = ret[1]
            schema_name = self.batch.sch.current_schema.schema_name
            schema_flat_name = self.get_flat_name(schema_name)
            ret_file_and_path += "simed_setup"+self.dir_separator
            if ver == 0:
                ver = self.batch.tsk.current_task.queue_ver
            file_version = self.comfun.str_with_zeros(ver, self.prj.current_project.zeros_in_version)
            file_ext = self.batch.dfn.get_current_setup_ext()
            ret_file_and_path += schema_flat_name + "__simed__v" + file_version + "." + file_ext
            return ret[0], ret_file_and_path
        return ret

    def generate_shot_cache_path(self):
        ret = self.generate_shot_dir()
        return ret[0], ret[1] + "cache"

    def generate_shot_cam_path(self):
        ret = self.generate_shot_dir()
        return ret[0], ret[1] + "cam"

    def generate_project_props_path(self):
        ret = self.generate_shot_dir()
        return ret[0], ret[1] + "props"

    def generate_shot_prev_file(self):
        ret = self.generate_shot_dir()
        if ret[0] == 1:
            ret_file_and_path = ret[1] + "prev" +self.dir_separator
            schema_name = self.batch.sch.current_schema.schema_name
            schema_flat_name = self.get_flat_name(schema_name)
            ver = self.batch.tsk.current_task.queue_ver
            file_version = self.comfun.str_with_zeros(ver, self.prj.current_project.zeros_in_version)
            file_ext = self.batch.dfn.get_current_prev_ext()
            ret_file_and_path += schema_flat_name + "__prev__v" + file_version + "__####." + file_ext
            return ret[0], ret_file_and_path
        return ret

    def generate_scripts_path(self):
        ret = self.generate_shot_dir()
        return ret[0], ret[1] + "scripts"


    #  get directory pattern for current project
    #  pattern is generated basis on directories structure on storage
    #  used for construct new path, generate path for load
    def get_dir_patterns(self, directory):
        self.batch.logger.db(("(get_dir_patterns) deep debug start dir:", directory))
        full_dir_pattern = None
        return full_dir_pattern


