import os

for i in range(1, 251):
    dir_ = 'output_batch_{}'.format(i)
    file_ = '/eos/cms/store/group/dpg_ecal/alca_ecalcalib/EcalTiming/Run2018D_UltraLegacy/Test/Calib/{}/{}ecal*'.format(dir_, dir_)
    cmd = 'rename {}ecal ecal {}'.format(dir_, file_)
    os.system(cmd)
