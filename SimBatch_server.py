
simbatch_config_ini = "/job/simbatch_test/config.ini"

import simbatch.core.core as simbatch_core

import simbatch.server.server as simbatch_server

# SBS = SimBatchServer( settings ,  Queue( settings ) ,  SimNodes( settings ),  soCo )



no_gui_batch = simbatch_core.SimBatch("Server", ini_file=simbatch_config_ini)
no_gui_batch.logger.console_level = 3


sim_batch_server = simbatch_server.SimBatchServer(no_gui_batch)
sim_batch_server.loopsLimit = 4
sim_batch_server.run()

# print "\n\nAFTER", sim_batch_server.last_info
