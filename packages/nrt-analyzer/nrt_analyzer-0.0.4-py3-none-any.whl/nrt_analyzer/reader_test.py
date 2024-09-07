from nrt_analyzer.definitions import NRTReader, plot_agf, plot_soe, get_soe_measures, get_files
from nrt_analyzer.data_storage_tools import SubjectInformation, MeasurementInformation, PandasDataTable, store_data
import pandas as pd


def my_pipe(file_name: str = '', database_path: str = ''):
    reader = NRTReader(file_name)
    reader.run()
    data_set = reader.responses
    groups = data_set.groupby(['measurement_type'])
    for (_m_t, ), _subset in groups:
        subject_info = SubjectInformation(subject_id='Test')
        measure_info = MeasurementInformation(experiment='NRT', condition='test', date='today')
        for _idx_row, _row in _subset.iterrows():
            # stimulus = _row[['Probe Active Electrode', 'N1_amp', 'P2_amp', 't_n1', 't_p2', 'rn', 'rn_ci', 'amp_ci',
            # 'alpha']]
            amp_items = ['N1_P2_amp', 'N1_amp', 'P2_amp', 't_n1', 't_p2', 'rn', 'rn_ci', 'amp_ci', 'alpha', 'amp_sig']
            amps = pd.DataFrame([_row[amp_items].to_dict()])
            amp_table = PandasDataTable(table_name='amplitudes', pandas_df=amps)
            waveforms_items = ['masker', 'probe', 'masker_probe', 'base_line', 'probe', 'ecap', 'time']
            wave_forms = pd.DataFrame([_row[waveforms_items].to_dict()])
            waveform_table = PandasDataTable(table_name='waveforms', pandas_df=wave_forms)
            keys = set(_row.keys())
            stimulus = _row[list(keys.difference(amp_items + waveforms_items))]
            rec_info = {'dummy': ''}
            store_data(database_path=database_path,
                       subject_info=subject_info,
                       measurement_info=measure_info,
                       recording_info=rec_info,
                       stimuli_info=stimulus.to_dict(),
                       pandas_df=[amp_table, waveform_table])

        if _m_t == "AGF":
            sub_groups = _subset.groupby(['Probe_Active_Electrode', 'Masker_Active_Electrode'])
            for (_p, _m), _sub_subset in sub_groups:
                fig = plot_agf(data_set=_sub_subset)
                fig.savefig(reader.paths.figure_basename_path + 'AGF_m{:}_p{:}'.format(_m, _p) + '.png')
        if _m_t == "SOE":
            sub_groups = _subset.groupby(['Masker_Active_Electrode'])
            measure_info = MeasurementInformation(experiment='SOE', condition='soe_condition', date='today')
            for (_m), _sub_subset in sub_groups:
                measures, clean_data_set = get_soe_measures(_sub_subset)
                keys = set(clean_data_set.keys())
                keys = keys.difference(amp_items + waveforms_items)
                _params = {}
                [_params.update({_key: clean_data_set[_key].unique()[0]}) for _key in keys if
                 clean_data_set[_key].unique().size == 1]

                measures_to_save = pd.DataFrame(measures[['width', 'centroid', 'ini_el', 'end_el']].to_dict())
                soe_table = PandasDataTable(table_name='soe_measures', pandas_df=measures_to_save)

                fig = plot_soe(measures=measures)
                fig.savefig(reader.paths.figure_basename_path + 'SOE_m{:}'.format(_m) + '.png')
                store_data(database_path=database_path,
                           subject_info=subject_info,
                           measurement_info=measure_info,
                           recording_info=rec_info,
                           stimuli_info=_params,
                           pandas_df=[soe_table])


if __name__ == "__main__":
    data_file = '../test_data/'
    database_path = '../test_data/data.sqlite'
    files = get_files(data_file)
    for _file in files:
        my_pipe(file_name=_file, database_path=database_path)
