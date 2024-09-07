import numpy as np
import h5py
import os
import json

class SpecialEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj._pmsname()
        except AttributeError:
            pass
        try:
            return obj._hdf5_outname()
        except AttributeError:
            pass
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class OutfileLeonardo(object):

    def __init__(self, filename):
        #
        # verify that the file does not exist
        self.filename = filename
        if os.path.exists(self.filename):
            self.readonly = True
            self.created = True
            self.read_run_parameters()
        else:
            self.readonly = False
            self.created = False

    def _hdf5_outname(self):
        str = '{}'.format(self.filename)
        return str

    #
    # This method is used to create the file and write the run_parameters, which are
    #   required to construct the directory structure
    def create_file(self, run_parameters):
        #
        f = h5py.File(self.filename, 'w-')
        #
        f['/'].attrs['run_parameters'] = json.dumps(run_parameters, cls=SpecialEncoder)
        #
        self.set_file_paths(run_parameters)
        #for ipop in range(run_parameters['npops']):
        #    f.create_dataset(self.pop_paths[ipop], data=arr, dtype=arr.dtype)
        #    f[self.pop_paths[ipop]].attrs['parameters'] = json.dumps(run_parameters, cls=SpecialEncoder)
        #    #for itime in run_parameters['ntimes']:
        #    #    for iyso in run_parameters['nysos']:
        #    #        pass
        #
        f.close()

        self.created = True

    #
    # This method is used to read run_parameters from the file, it also
    #   calls the self.set_file_paths to construct the directory structure
    def read_run_parameters(self):
        #
        if self.created:
            f = h5py.File(self.filename, 'r')
            run_parameters = json.loads(f['/'].attrs['run_parameters'])
            f.close()
        else:
            raise ValueError("File {} not yet created".format(self.filename))

        self.set_file_paths(run_parameters)

        return run_parameters

    #
    # This method is used to construct the directory structure from run_parameters
    def set_file_paths(self, run_parameters):

        self.pop_paths = []
        self.time_paths_list = []
        self.yso_paths_list = []
        self.star_paths_list = []
        self.disc_paths_list = []

        for ipop in range(run_parameters['npops']):

            mypop = 'pop_' + str(ipop)
            self.pop_paths.append(os.path.join("/", mypop))
            time_paths = []
            yso_paths_time = []
            star_paths_time = []
            disc_paths_time = []

            for itime in range(run_parameters['ntimes']):

                mytime = 'time_'+str(itime)
                time_paths.append(os.path.join(self.pop_paths[-1], mytime))
                yso_paths = []
                star_paths = []
                disc_paths = []

                for iyso in range(run_parameters['nysos']):

                    myyso = 'yso_' + str(iyso)
                    yso_paths.append(os.path.join(time_paths[-1], myyso))
                    star_paths.append(os.path.join(yso_paths[-1], 'Star'))
                    disc_paths.append(os.path.join(yso_paths[-1], 'Disc'))

                yso_paths_time.append(yso_paths)
                star_paths_time.append(star_paths)
                disc_paths_time.append(disc_paths)

            self.time_paths_list.append(time_paths)
            self.yso_paths_list.append(yso_paths_time)
            self.star_paths_list.append(star_paths_time)
            self.disc_paths_list.append(disc_paths_time)

    #
    # Method to write attributes
    def write_data_to_hdf5(self, path, data_dict, attributes):
        #
        if self.created and not self.readonly:
            f = h5py.File(self.filename, 'a')
            for key in data_dict:
                f.create_dataset(os.path.join(path, key), data=np.array(data_dict[key]), dtype=np.array(data_dict[key]).dtype)
            f[path].attrs['headers'] = json.dumps(attributes, cls=SpecialEncoder)
            f.close()
        else:
            raise ValueError("Input file {} not yet created or readonly".format(self.filename))

    #
    # Method to read attributes
    def read_data_from_hdf5(self, path):
        #
        if os.path.isfile(self.filename):
            f = h5py.File(self.filename, 'r')
            item = f[path]
            attributes = json.loads(item.attrs['headers'])
            ndat = 0
            for field in item.keys():
                if isinstance(item[field], h5py.Dataset):
                    if ndat == 0:
                        data_dict = {field: item[field][()]}
                    else:
                        data_dict[field] = item[field][()]
                    ndat += 1
            f.close()
            return data_dict, attributes
        else:
            raise ValueError("Input file {} not created".format(self.filename))


def save_to_hdf5(filename, data, path, headers=None, field_names=None,
                 root_headers=None, filemode="a"):
    """
    Saves a list of arrays as a group of datasets in an HDF5 file.

    Parameters
    ----------
    filename : str
        Full name of the HDF5 file, including extension ".hdf5".
        The files are opened in "append" mode as default.
    data : list of ndarrays
        The list of ndarrays is stored as an HDF5 group.
        Each ndarray is stored as an HDF5 dataset.
        ndarrays can have different dtypes.
    path : str
        Absolute path of the group in the HDF5 file.
    headers : dict, optional
        Headers to be stored as attributes of the group.
    field_names : list of str, optional
        Names of the arrays, in the same order as in `data`.
        Each array is stored as dataset with name
    root_headers : dict, optional


    Examples
    --------
    filename = 'test.hdf5'

    # list of arrays (e.g. outputs of a snapshot)

    # example arrays
    arrs = [np.ones(10, dtype='int'), 
            np.zeros(20, dtype='float64'), 
            2*np.ones(30, dtype='float32')] 

    # example header of the current arrays
    h = dict(snapshot={'time': 1000., 'units': 'bla bla'})

    # example root headers of the whole compution
    root_h = dict(disc={'a': 2}, star={'b': 1.2, 'c': [0.3, 2., 1.]})

    # example path for a snapshot
    num = 1
    sub_path = '/snapshots/{}'.format(num)

    save_to_hdf5(filename, arrs, h, sub_path, 
                 field_names=['radius', 'sigma', 'temp'], root_headers=root_h)

    """
        
    if field_names:
        assert len(data) == len(
            field_names), "number of field_names does not match number of arrays in data"
    else:
        field_names = ['Field_{}'.format(j) for j in range(len(data))]

    try:
        f = h5py.File(filename, filemode)
        assert path not in f.keys(),\
            "Path '{}' is already present in the HDF5 file '{}'".format(path,
                                                                    filename)

        if root_headers:
            f['/'].attrs['headers'] = json.dumps(root_headers, cls=SpecialEncoder)
        else:
            f['/'].attrs['headers'] = ''

        for i, arr in enumerate(data):
            f.create_dataset(os.path.join(path, field_names[i]), data=arr, dtype=arr.dtype)

        if headers:
            f[path].attrs['headers'] = json.dumps(headers, cls=SpecialEncoder)
        else:
            f[path].attrs['headers'] = ''

    except:
        f.close()
        raise

    else:
        f.close()


def save_snapshot(filename, evolver):
    """
    Saves a snapshot to an HDF5 file.

    :param filename:
    :param evolver:
    :return:
    """
    print(evolver.parameters['yso']['yso_id'], evolver.evolution_time)
    save_to_hdf5(filename, [evolver.R, evolver.sigma, evolver.T],
                 os.path.join("{}".format(evolver.parameters['yso']['yso_id']),
                              os.path.join("snapshots", str(evolver.evolution_time))),
                 headers=evolver.status,
                 field_names=['R', 'sigma', 'T'],
                 root_headers=evolver.parameters)


def read_snapshots(filename):
    """
    Reads the snapshots contained in an HDF5 file.

    Parameters
    ----------
    filename : str
        File name of the HDF5 file, including ".hdf5".

    Note: JSON decoding is needed to convert headers back from str to dict.

    Returns
    -------
    A dictionary, containing:

    snapshots : dict
        Contains the snapshots: the timestamp is the dictionary key to access them.
        Each snapshot contains data (a dict containing the fields with their names),
        and headers.
    root_headers : dict
        Root headers of the simulation.

    """
    f = h5py.File(filename, 'r')

    root_headers = json.loads(f['/'].attrs['headers'])

    N_objects = 10  # root_headers['']

    snapshots = []
    for i in range(N_objects):
        data = f[str(i)]['snapshots']

        snapshots.append({snapshot: {'data': {field: data[snapshot][field][()] for field in data[snapshot].keys()},
                          'headers': json.loads(data[snapshot].attrs['headers'])}
                     for snapshot in data.keys()})

    f.close()

    return {'snapshots': snapshots, 'root_headers': root_headers}


def test_save_to_hdf5():
    """
    To be removed, for development only.
    Tests the save_to_hdf5() function.
    You can open the output file for inspection.

    """
    filename = 'test.hdf5'

    # list of arrays (e.g. outputs of a snapshot)

    # example arrays
    arrs = [np.ones(10, dtype='int'), np.zeros(20, dtype='float64'),
            2 * np.ones(30, dtype='float32')]

    # example header of the current arrays
    h = dict(snapshot={'time': 1000., 'units': 'bla bla'})

    # example root headers of the whole compution
    root_h = dict(disc={'a': 2}, star={'b': 1.2, 'c': [0.3, 2., 1.]})

    # example path for a snapshot
    num = 2
    sub_path = '/snapshots/{}'.format(num)

    save_to_hdf5(filename, arrs, h, sub_path,
                 field_names=['radius', 'sigma', 'temp'], root_headers=root_h)


def test_read_snapshots():
    """
    Tests the read_from_hdf5() function.
    Reads the HDF5 output of a run, and produces control plots for two quantities.

    """
    import matplotlib.pyplot as plt

    filename = 'Pop_3.hdf5'
    loaded = read_snapshots(filename)

    print(type(loaded['root_headers']))
    snapshots = loaded['snapshots']
    print(snapshots['13000000.0']['data'].keys())
    for timestamp in snapshots.keys():
        plt.loglog(snapshots[timestamp]['data']['R'], snapshots[timestamp]['data']['sigma'],
                   label='{:5.2e}'.format(np.float(timestamp)))
        plt.xlabel('R (au)')
        plt.ylabel('Sigma (g cm-2)')

    plt.legend(frameon=False)
    plt.tight_layout()
    plt.show()

    for timestamp in snapshots.keys():
        plt.loglog(snapshots[timestamp]['data']['R'], snapshots[timestamp]['data']['T'],
                   label='{:5.2e}'.format(np.float(timestamp)))
        plt.xlabel('R (au)')
        plt.ylabel('T (K)')

    plt.legend(frameon=False)
    plt.tight_layout()
    plt.show()


