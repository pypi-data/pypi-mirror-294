import pandas as pd
import numpy as np
from sklearn.linear_model import HuberRegressor
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.signal import resample
from matplotlib.pyplot import cm
import os
from os.path import sep
import shutil
from pathlib import Path
import re


class NRTReader(object):
    def __init__(self, file_path: str = None, figures_subset_folder: str = '',
                 alpha=0.001,
                 upsampling_factor=10,
                 time_window: np.array = np.array([100e-6, 600e-6])  # in seconds
                 ):
        self.file_path = file_path
        self.output_node = None
        self.figures_subset_folder = figures_subset_folder
        self.paths = DirectoryPaths(file_path=self.file_path,
                                    delete_all=False, delete_figures=False,
                                    figures_subset_folder=figures_subset_folder)
        self.responses = None
        self.alpha = alpha
        self.upsampling_factor = upsampling_factor
        self.time_window = time_window

    def run(self):
        # we check that sheets exits
        try:
            _tmp = pd.ExcelFile(self.file_path)
        except Exception as e:
            str(e)
            return

        _tmp.sheet_names  # see all sheet names
        if ("NRT Series" not in _tmp.sheet_names) or ("NRT Buffers" not in _tmp.sheet_names):
            return
        df_descriptor = pd.read_excel(self.file_path, sheet_name="NRT Series", skiprows=[0])
        # remove spaces from columns
        new_cols = [re.sub(r'[\s]', '_', _col) for _col in df_descriptor.keys()]
        new_cols = [re.sub(r'\((.*)\)', '\\1', _col) for _col in new_cols]
        _replace_dict = {}
        for _old, _new in zip(df_descriptor.keys(), new_cols):
            _replace_dict[_old] = _new
        df_descriptor = df_descriptor.rename(columns=_replace_dict)

        df_nrt_buffers = pd.read_excel(self.file_path, sheet_name="NRT Buffers", skiprows=[])
        new_cols = [re.sub(r'[\s]', '_', _col) for _col in df_nrt_buffers.keys()]
        new_cols = [re.sub(r'\((.*)\)', '\\1', _col) for _col in new_cols]
        _replace_dict = {}
        for _old, _new in zip(df_nrt_buffers.keys(), new_cols):
            _replace_dict[_old] = _new
        df_nrt_buffers = df_nrt_buffers.rename(columns=_replace_dict)
        # combine data frames
        data = df_descriptor.join(df_nrt_buffers.set_index('NRT_Nr'), on='NRT_Number')
        # remove data without measurements
        nrt_nr_to_remove = data[data['Sample_µV'].isna()]['NRT_Number'].unique()
        data = data[~data.NRT_Number.isin(nrt_nr_to_remove)]
        df_descriptor = df_descriptor[~df_descriptor.NRT_Number.isin(nrt_nr_to_remove)]
        data = data.sort_values(by=['Probe_Current_Level', 'Frame_type'], ascending=False)
        df_descriptor['ecap'] = None
        df_descriptor['masker'] = None
        df_descriptor['probe'] = None
        df_descriptor['probe_mode'] = None
        df_descriptor['masker_mode'] = None
        df_descriptor['masker_probe'] = None
        df_descriptor['base_line'] = None
        df_descriptor['time'] = None
        df_descriptor['alpha'] = self.alpha
        df_descriptor['upsampling_factor'] = self.upsampling_factor
        df_descriptor['measurement_type'] = None
        groups = data.groupby(['NRT_Number',
                               'Probe_Active_Electrode',
                               'Masker_Active_Electrode',
                               'Probe_Rate',
                               'Masker_Rate'])
        for (_number, _p, _m, _r_p, _r_m), _condition in groups:
            if _condition.shape[0] <= 1:
                continue
            n_samples_block = int(np.unique(_condition["Nr_of_Samples"]))
            probe = _condition.query('`Frame_type` == "{:}"'.format("A"))['Sample_µV'].to_numpy().reshape(-1, 1)
            masker_probe = _condition.query('`Frame_type` == "{:}"'.format("B"))['Sample_µV'].to_numpy().reshape(-1, 1)
            masker = _condition.query('`Frame_type` == "{:}"'.format("C"))['Sample_µV'].to_numpy().reshape(-1, 1)
            base_line = _condition.query('`Frame_type` == "{:}"'.format("D"))['Sample_µV'].to_numpy().reshape(-1, 1)
            time = _condition['Time_µs'].to_numpy()
            time = time[0:n_samples_block].reshape(-1, 1)
            nrt = probe - (masker_probe - masker) - base_line
            # get status of recordings
            status_probe = self.get_status(
                _condition.query('`Frame_type` == "{:}"'.format("A"))['Status'].unique())
            status_masker_probe = self.get_status(
                _condition.query('`Frame_type` == "{:}"'.format("B"))['Status'].unique())
            status_masker = self.get_status(
                _condition.query('`Frame_type` == "{:}"'.format("C"))['Status'].unique())
            status_base_line = self.get_status(
                _condition.query('`Frame_type` == "{:}"'.format("D"))['Status'].unique())

            # upsampling data to improve peak resolution
            _nrt = np.vstack((np.flip(nrt, axis=0), nrt, np.flip(nrt, axis=0)))
            fs = 1 / np.mean(np.diff(time * 1e-6, axis=0), 0)[0]
            time = np.arange(0, _nrt.size) / fs * 1e6
            time = time - time[nrt.size]
            fs_factor = self.upsampling_factor
            _nrt, _time = resample(_nrt, num=int(fs_factor * _nrt.size), t=time)
            _ini = nrt.size * fs_factor
            _end = 2 * nrt.size * fs_factor
            nrt = _nrt[_ini: _end]
            time = _time[_ini: _end]
            nrt -= np.mean(nrt)
            time = time.reshape(-1, 1)
            # find peaks above time limit
            time_samples = self.time_window * fs * fs_factor
            time_samples = np.minimum(np.maximum(0.0, time_samples), nrt.shape[0]).astype(int)
            _v = np.arange(time_samples.min(), time_samples.max())
            n1_idx = np.where(nrt[_v] == np.min(nrt[_v]))[0] + time_samples.min()
            p2_idx = np.where(nrt[n1_idx[0]::] == np.max(nrt[n1_idx[0]::]))[0]
            p2_idx += n1_idx
            # estimate noise from last quarter of the recording
            _ini_sample = int(time.size * 0.6)
            reg = HuberRegressor().fit(time[_ini_sample::].reshape(-1, 1), nrt[_ini_sample::].reshape(-1, ))

            rn = np.std(nrt[_ini_sample::] - reg.predict(time[_ini_sample::]).reshape(-1, 1))

            _idx_item = np.logical_and(np.logical_and(df_descriptor['NRT_Number'] == _number,
                                                      df_descriptor['Probe_Active_Electrode'] == _p),
                                       df_descriptor['Masker_Active_Electrode'] == _m)

            _the_index = int(np.argwhere(_idx_item))
            df_descriptor.at[_the_index, 'masker'] = masker
            df_descriptor.at[_the_index, 'probe'] = probe
            df_descriptor.at[_the_index, 'masker_probe'] = masker_probe
            df_descriptor.at[_the_index, 'base_line'] = base_line
            df_descriptor.at[_the_index, 'status_masker'] = status_masker
            df_descriptor.at[_the_index, 'status_probe'] = status_probe
            df_descriptor.at[_the_index, 'status_masker_probe'] = status_masker_probe
            df_descriptor.at[_the_index, 'status_base_line'] = status_base_line
            df_descriptor.at[_the_index, 'ecap'] = nrt
            df_descriptor.at[_the_index, 'time'] = time
            df_descriptor.at[_the_index, 'fs'] = fs
            df_descriptor.at[_the_index, 'rn'] = rn
            df_descriptor.at[_the_index, 't_n1'] = time[n1_idx]
            df_descriptor.at[_the_index, 't_p2'] = time[p2_idx]
            df_descriptor.at[_the_index, 'N1_P2_amp'] = nrt[p2_idx] - nrt[n1_idx]
            df_descriptor.at[_the_index, 'N1_amp'] = nrt[n1_idx]
            df_descriptor.at[_the_index, 'P2_amp'] = nrt[p2_idx]
            sig_factor = np.abs(st.norm.ppf(self.alpha / 2))
            amp_ci = sig_factor * np.sqrt(2 * rn ** 2.0)
            df_descriptor.at[_the_index, 'amp_ci'] = amp_ci
            df_descriptor.at[_the_index, 'amp_sig'] = bool(np.squeeze(np.abs(nrt[p2_idx] - nrt[n1_idx]) > amp_ci))
            rn_ci = sig_factor * rn
            df_descriptor.at[_the_index, 'rn_ci'] = rn_ci

            if df_descriptor.loc[_the_index, 'Probe_Indifferent_Electrode'] in ['MP1', 'MP2', 'MP1+2']:
                df_descriptor.at[_the_index, 'probe_mode'] = 'MP'
            else:
                df_descriptor.at[_the_index, 'probe_mode'] = 'BP'
            if df_descriptor.loc[_the_index, 'Masker_Indifferent_Electrode'] in ['MP1', 'MP2', 'MP1+2']:
                df_descriptor.at[_the_index, 'masker_mode'] = 'MP'
            else:
                df_descriptor.at[_the_index, 'masker_mode'] = 'BP'
        # df_descriptor['Probe_Indifferent_Electrode'] = df_descriptor['Probe_Indifferent_Electrode'].astype(str)
        # df_descriptor['Masker_Indifferent_Electrode'] = df_descriptor['Masker_Indifferent_Electrode'].astype(str)
        # classify AGF measurements
        groups = df_descriptor.groupby(['Probe_Active_Electrode', 'Masker_Active_Electrode'])
        for (_p, _m), _condition in groups:
            if ((_condition.shape[0] > 1) and (_condition['Probe_Current_Level'].unique().size ==
                                               _condition['Probe_Current_Level'].size)):
                df_descriptor.loc[_condition.index, 'measurement_type'] = 'AGF'
        # classify SOE measurements
        groups = df_descriptor.groupby(['Masker_Active_Electrode'])
        for (_m), _condition in groups:
            if ((_condition.shape[0] > 1) and
                    (_condition['Probe_Active_Electrode'].unique().size == _condition['Probe_Active_Electrode'].size)):
                df_descriptor.loc[_condition.index, 'measurement_type'] = 'SOE'

        groups = df_descriptor.groupby(['Probe_Active_Electrode'])
        for (_p), _condition in groups:
            if ((_condition.shape[0] > 1) and
                    (_condition['Masker_Active_Electrode'].unique().size == _condition[
                        'Masker_Active_Electrode'].size)):
                df_descriptor.loc[_condition.index, 'measurement_type'] = 'SOE'
        df_descriptor = df_descriptor.dropna()
        self.responses = df_descriptor

    @staticmethod
    def get_status(status_list: [str] = None):
        status = 'ok'
        for _c in status_list:
            _value = str(_c)
            if _value == 'X':
                status = 'clipped'
            if _value == 'O':
                status = 'compliance'
        return status


class DirectoryPaths(object):
    def __init__(self, file_path='', delete_all=False, delete_figures=False, figures_subset_folder=''):
        self.file_path = file_path
        self.file_directory = os.path.dirname(os.path.realpath(file_path))
        self.file_basename_path = os.path.splitext(file_path)[0]
        self.delete_all = delete_all
        self.delete_figures = delete_figures
        figures_dir = os.path.join(self.file_directory, 'figures')
        if (self.delete_all or self.delete_figures) and os.path.exists(figures_dir):
            try:
                shutil.rmtree(figures_dir)
            except OSError:
                print((OSError.message))
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)
        self.figures_dir = figures_dir

        data_directory = os.path.join(self.file_directory, '.data')
        if self.delete_all and os.path.exists(data_directory):
            try:
                shutil.rmtree(data_directory)
            except OSError:
                print(OSError.message)
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        self.data_dir = data_directory
        self.subset_identifier = figures_subset_folder

    def get_figure_basename_path(self):
        return os.path.join(self.figure_subset_path, os.path.basename(self.file_path).split('.')[0])

    figure_basename_path = property(get_figure_basename_path)

    def get_data_basename_path(self):
        return os.path.join(self.data_subset_path, os.path.basename(self.file_path).split('.')[0])

    data_basename_path = property(get_data_basename_path)

    def get_figure_subset_path(self):
        _path = os.path.join(self.figures_dir, self.subset_identifier) + sep
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path

    figure_subset_path = property(get_figure_subset_path)

    def get_data_subset_path(self):
        _path = os.path.join(self.data_dir, self.subset_identifier)
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path

    data_path = property(get_data_subset_path)
    figures_current_dir = property(get_figure_subset_path)


def get_files(path: str = ''):
    files = []
    for path in Path(path).rglob('*.xlsx'):
        files.append(str(path))
        print(path.name)
    return files


def plot_agf(data_set: pd.DataFrame = None):
    fig_out = plt.figure(constrained_layout=False)
    gs = gridspec.GridSpec(nrows=1, ncols=2, hspace=0.1, wspace=0.2)
    ax = plt.subplot(gs[0, 0])
    el_probe = data_set['Probe_Active_Electrode'].unique()[0]
    color = iter(cm.viridis(np.linspace(0, 1, data_set.shape[0])))
    for _idx_row, _condition_nrt in data_set.iterrows():
        nrt = _condition_nrt['ecap']
        time = _condition_nrt['time']
        c = next(color)
        plt.plot(time, nrt, color=c)
        sig = _condition_nrt['amp_sig']
        if sig:
            marker_color = None
        else:
            marker_color = 'white'

        marker_style = dict(markersize=6)

        ax.plot(_condition_nrt['t_n1'], _condition_nrt['N1_amp'], marker='v', markerfacecolor=marker_color, color=c,
                **marker_style)
        ax.plot(_condition_nrt['t_p2'], _condition_nrt['P2_amp'], marker='^', markerfacecolor=marker_color, color=c,
                **marker_style)
    ax.set_ylabel('Amplitude [uV]')
    ax.set_xlabel('Time [us]')
    ax.axhline(data_set['rn_ci'].max() / 2, color='gray')
    ax.axhline(-data_set['rn_ci'].max() / 2, color='gray')
    ax = plt.subplot(gs[0, 1])
    color = iter(cm.viridis(np.linspace(0, 1, data_set.shape[0])))
    for _cu, _amp, _sig in zip(data_set['Probe_Current_Level'], data_set['N1_P2_amp'], data_set['amp_sig']):
        _c = next(color)
        marker_color = _c
        if not _sig:
            marker_color = 'white'
        ax.plot(_cu, _amp, 'o', color=_c, markerfacecolor=marker_color)
    ax.errorbar(data_set['Probe_Current_Level'], data_set['N1_P2_amp'],
                yerr=data_set['amp_ci'] / 2,
                label='EL: {:}'.format(el_probe))
    ax.fill_between(data_set['Probe_Current_Level'], data_set['amp_ci'] * 0, data_set['amp_ci'],
                    where=data_set['amp_ci'] >= data_set['amp_ci'] * 0,
                    facecolor='gray', alpha=0.3)
    ax.set_xlabel('CU')
    ax.legend()
    fig_out.suptitle('{:} Masker {:} cu / {:} Probe'.format(data_set.masker_mode.unique()[0],
                                                            data_set.Masker_Current_Level.unique()[0],
                                                            data_set.probe_mode.unique()[0]))
    return fig_out


def get_soe_measures(data_set: pd.DataFrame = None):
    data_set = data_set[data_set.Recording_Active_Electrode.astype(str) != data_set.Probe_Active_Electrode.astype(str)]
    data_set = data_set[
        data_set.Recording_Active_Electrode.astype(str) != data_set.Probe_Indifferent_Electrode.astype(str)]
    data_set = data_set[data_set.Recording_Active_Electrode.astype(str) != data_set.Masker_Active_Electrode.astype(str)]
    data_set = data_set[
        data_set.Recording_Active_Electrode.astype(str) != data_set.Masker_Indifferent_Electrode.astype(str)]
    data_set = data_set.dropna(subset=['ecap'])

    el_mask = data_set['Masker_Active_Electrode'].unique()
    if el_mask.size > 1:
        moving_active_electrode = data_set['Masker_Active_Electrode']
        moving_indifferent_electrode = data_set['Masker_Indifferent_Electrode']
        fixed_active_electrode = data_set['Probe_Active_Electrode']
        fixed_indifferent_electrode = data_set['Probe_Indifferent_Electrode']
    else:
        moving_active_electrode = data_set['Probe_Active_Electrode']
        moving_indifferent_electrode = data_set['Probe_Indifferent_Electrode']
        fixed_active_electrode = data_set['Masker_Active_Electrode']
        fixed_indifferent_electrode = data_set['Masker_Indifferent_Electrode']

    centroid = np.sum(moving_active_electrode * data_set['N1_P2_amp']) / np.sum(data_set['N1_P2_amp'])
    # compute width and plot cumulative sum
    _c_sum = np.cumsum(data_set['N1_P2_amp'])
    _c_sum /= _c_sum.max()

    _width, x_ini, x_end = compute_width(x=moving_active_electrode.to_numpy(), y=_c_sum.to_numpy())
    _data = {'width': _width,
             'ini_el': x_ini,
             'end_el': x_end,
             'cum_sum': _c_sum,
             'centroid': centroid,
             'moving_active_electrode': moving_active_electrode,
             'moving_indifferent_electrode': moving_indifferent_electrode,
             'fixed_active_electrode': fixed_active_electrode,
             'fixed_indifferent_electrode': fixed_indifferent_electrode,
             'N1_P2_amp': data_set['N1_P2_amp'],
             'amp_ci': data_set['amp_ci'],
             'rn_ci': data_set['rn_ci'],
             'rn': data_set['rn'],
             'ecap': data_set['ecap'],
             'time': data_set['time'],
             't_n1': data_set['t_n1'],
             'N1_amp': data_set['N1_amp'],
             't_p2': data_set['t_p2'],
             'P2_amp': data_set['P2_amp'],
             'amp_sig': data_set['amp_sig'],
             'masker_level': data_set['Masker_Current_Level'],
             'probe_level': data_set['Probe_Current_Level'],
             'masker_mode': data_set['masker_mode'],
             'probe_mode': data_set['probe_mode'],
             'rec_el': data_set['Recording_Active_Electrode']
             }
    data = pd.Series(_data)
    return data, data_set


def plot_soe(measures: pd.Series = None):
    fig_out = plt.figure(constrained_layout=False)
    gs = gridspec.GridSpec(nrows=2, ncols=int(measures.moving_active_electrode.max()), hspace=0.2)
    amp_max = measures.N1_P2_amp.max()
    amp_n1_min = measures.N1_amp.min()
    amp_p2_max = measures.P2_amp.max()
    for _idx, (N1_P2_amp,
               m_a_el,
               m_r_el,
               f_a_el,
               f_r_el,
               nrt,
               time,
               rn_ci,
               t_n1,
               t_p2,
               N1_amp,
               P2_amp,
               amp_sig,
               rec_el) in enumerate(zip(measures.N1_P2_amp,
                                        measures.moving_active_electrode,
                                        measures.moving_indifferent_electrode,
                                        measures.fixed_active_electrode,
                                        measures.fixed_indifferent_electrode,
                                        measures.ecap, measures.time,
                                        measures.rn_ci,
                                        measures.t_n1, measures.t_p2,
                                        measures.N1_amp, measures.P2_amp,
                                        measures.amp_sig,
                                        measures.rec_el)):
        ax = plt.subplot(gs[0, int(m_a_el) - 1])
        if ((str(f_a_el) == str(m_a_el)) or
                (str(f_r_el) == str(m_a_el)) or
                (str(f_a_el) == m_r_el)):
            plt.plot(time, nrt, color="red")
        else:
            plt.plot(time, nrt)
        if amp_sig:
            marker_color = None
        else:
            marker_color = 'white'

        marker_style = dict(markersize=6)

        ax.plot(t_n1, N1_amp, marker='v', markerfacecolor=marker_color, **marker_style)
        ax.plot(t_p2, P2_amp, marker='^', markerfacecolor=marker_color, **marker_style)
        ax.set_ylim(1.5 * amp_n1_min, 1.5 * amp_p2_max)
        ax.set_xlabel('{:}'.format(m_a_el))
        ax.set_ylabel('Amplitude [uV]')
        ax.axhline(rn_ci / 2, color='gray')
        ax.axhline(-rn_ci / 2, color='gray')

    fig_out.suptitle('{:} Masker {:}cu / {:} Probe {:}cu'.format(
        measures.masker_mode.unique()[0],
        measures.masker_level.unique()[0],
        measures.probe_mode.unique()[0],
        measures.probe_level.unique()[0]))
    all_axes = fig_out.get_axes()
    for ax in all_axes:
        ax.spines['top'].set_visible(False)
        if not ax.get_subplotspec().is_last_row():
            ax.set_xticklabels([])
            ax.set_xticks([])
        if not ax.get_subplotspec().is_first_col():
            ax.spines['left'].set_visible(False)
            ax.set_yticklabels([])
            ax.set_ylabel('')
        ax.spines['right'].set_visible(False)

    ax = plt.subplot(gs[1, ::])
    ax.errorbar(measures.moving_active_electrode, measures.N1_P2_amp, yerr=measures.amp_ci / 2)
    ax.fill_between(measures.moving_active_electrode, measures.amp_ci * 0, measures.amp_ci,
                    where=measures.amp_ci >= measures.amp_ci * 0,
                    facecolor='gray', alpha=0.3)
    ax.set_xlabel('Active Electrode')
    ax.set_ylabel('Amplitude [uV]')
    ax.set_xlim([1 - 0.5, measures.moving_active_electrode.max() + 0.5])
    ax.set_xticks(np.arange(1, measures.moving_active_electrode.max() + 1, 1.0))
    # plot centroid
    ax.plot(measures.centroid, 0, 'o', color='k')

    # plot active and reference electrodes
    ax.plot(measures.fixed_active_electrode.unique(),
            measures.fixed_active_electrode.unique() * 0, '+', color='r')

    if measures.masker_mode.unique() == 'BP':
        ax.plot(measures.fixed_indifferent_electrode.unique().astype(float),
                measures.fixed_indifferent_electrode.unique() * 0, '_', color='b')
    ax.plot(measures.rec_el.unique(),
            measures.rec_el.unique() * 0, '2', color='k')

    # plot cumulative sum
    ax.plot(measures.moving_active_electrode, measures.cum_sum * amp_max, color='gray', alpha=0.25)
    ax.plot([measures.ini_el, measures.ini_el], np.array([0, 0.25]) * amp_max, color='grey', alpha=0.25)
    ax.plot([measures.end_el, measures.end_el], np.array([0, 0.75]) * amp_max, color='gray', alpha=0.25)
    ax.plot([measures.ini_el, measures.end_el], np.array([0.25, 0.25]) * amp_max, color='gray', alpha=0.25)

    return fig_out


def find_point(x: np.array = None, y: np.array = None, y_target: float = None):
    _idx_0 = np.argwhere(y < y_target)[-1]
    _idx_1 = np.argwhere(y > y_target)[0]
    y_0 = y[_idx_0]
    y_1 = y[_idx_1]
    x_0 = x[_idx_0]
    x_1 = x[_idx_1]
    m = (y_1 - y_0) / (x_1 - x_0)
    x_target = (y_target - y_0) / m + x_0
    return x_target


def compute_width(x: np.array = None, y: np.array = None, y_ini: float = 0.25, y_end: float = 0.75):
    x1 = find_point(x=x, y=y, y_target=y_ini)
    x2 = find_point(x=x, y=y, y_target=y_end)
    return x2 - x1, x1, x2
