import time
import numpy as np


class CQDSpectrum:
    """Class describing a series of one or more spectra from a Carbon Quantum Dot sample"""

    # Class level attributes for background subtraction
    bg_abs_x = None
    bg_abs_y = None
    bg_ex350_x = None
    bg_ex350_ys = {}
    bg_ex400_x = None
    bg_ex400_ys = {}

    def __init__(self, wl_vector, y_vectors, meta_data):
        self.wl_vector = wl_vector  # numpy array of wavelength values
        self.y_vectors = y_vectors  # dictionary of numpy arrays containing y-value (absorbance or fluorescence)
        self.meta_data = meta_data  # dictionary containing metadata of spectra

    @classmethod
    def spectrum_from_xl_data(cls, start_t, end_t, attrib_col, value_col, rows):
        """
        Creates a CQDSpectrum object from data extracted from an excel file
        :param start_t: String: start time of measurement
        :param end_t: String: end time of measurement
        :param attrib_col: List: attributes of measurement
        :param value_col: List: values corresponding to attributes of measurement
        :param rows: List[List]: rows of spectral data
        :return: CQDSpectrum object
        """
        mode = value_col[attrib_col.index('Mode')]
        if mode == 'Absorbance':
            mode = 'Abs'
        elif mode == 'Fluorescence Top Reading':
            mode = 'Flu'
        else:
            print('{} is not a valid mode'.format(mode))
            return None

        meta_data = {'start_t': time.strptime(start_t, '%Y-%m-%d %H:%M:%S'),
                     'end_t': time.strptime(end_t, '%Y-%m-%d %H:%M:%S')}
        wl_vector = row_to_np_array(rows[0])
        y_vectors = {}
        if mode == 'Abs':
            y_vectors = {'Abs': row_to_np_array(rows[1])}
        elif mode == 'Flu':
            meta_data['gain'] = value_col[attrib_col.index('Gain')]
            meta_data['ex_wl'] = value_col[attrib_col.index('Excitation Wavelength')]
            y_vectors = {'Aq': row_to_np_array(rows[1]),
                         'Cu': row_to_np_array(rows[2]),
                         'Fe': row_to_np_array(rows[3]),
                         'Cd': row_to_np_array(rows[4])}

        return CQDSpectrum(wl_vector, y_vectors, meta_data)

    def subtracted(self, spec_key=None):
        """
        Performs background subtraction and returns y_vectors.
        If spec_key specified returns only spectrum for the given key.
        :param spec_key:
        :return: dict{key: Numpy.array} or Numpy.array if spec_key specified
        """
        spectra = self.y_vectors
        if spec_key is not None:
            spectra = {spec_key: self.y_vectors[spec_key]}

        # Absorbance spectrum
        if 'gain' not in self.meta_data:
            if CQDSpectrum.bg_abs_x is None:
                raise ValueError('Background spectrum is not initialized')

            if spec_key is not None:
                return spectra['Abs'] - CQDSpectrum.bg_abs_y
            return {'Abs': spectra['Abs'] - CQDSpectrum.bg_abs_y}

        # Fluorescence spectrum
        bg_ys = None
        if self.meta_data['ex_wl'] == 350:
            if CQDSpectrum.bg_ex350_x is None:
                raise ValueError('Background spectra ex350 is not initialized')
            bg_ys = CQDSpectrum.bg_ex350_ys
        if self.meta_data['ex_wl'] == 400:
            if CQDSpectrum.bg_ex400_x is None:
                raise ValueError('Background spectra ex400 is not initialized')
            bg_ys = CQDSpectrum.bg_ex400_ys

        gain = self.meta_data['gain']
        if gain in bg_ys:
            bg_ys = bg_ys[gain]
        else:
            keys = list(bg_ys.keys())
            try:
                over = min([x for x in keys if x > gain])
                under = max([x for x in keys if x < gain])
            except ValueError:
                print('Sample gain={} out of range for subtraction. Returning original spectra.'.format(gain))
                return spectra
            combined = {}
            for k in spectra.keys():
                low = bg_ys[under][k]
                high = bg_ys[over][k]
                com_y = low + (high-low) * ((gain-under)/(over-under))
                combined[k] = com_y
            bg_ys = combined

        subbed = {}
        for k in spectra.keys():
            subbed[k] = spectra[k]-bg_ys[k]

        if spec_key is not None:
            return subbed[spec_key]
        return subbed


def row_to_np_array(row: list) -> object:
    """
    Utility function that converts a list of values from an Excel worksheet to a numpy array
    :param row: list of cell values from an Excel worksheet
    :return: numpy array
    """
    row = row[1:]
    i = 0
    for c in row:
        if c == 'OVER':
            row[i] = 'Nan'
        if c == '':
            row = row[:i]
            break
        i += 1
    return np.array(row, dtype=float)
