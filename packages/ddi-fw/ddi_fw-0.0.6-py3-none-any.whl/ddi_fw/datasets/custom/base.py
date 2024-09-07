import pathlib
import numpy as np

import pandas as pd
from ..idf_helper import IDF

from ddi_fw.utils.zip_helper import ZipHelper
from .. import BaseDataset
from ..db_utils import create_connection

HERE = pathlib.Path(__file__).resolve().parent

'''
uses drugbank_db.zip
'''


class CustomDataset(BaseDataset):
    def __init__(self,  index_path, chemical_property_columns=['enzyme',
                                             'target',
                                             'pathway',
                                             'smile'],
                 drugbank_ids=[],
                 embedding_columns=['indication'],
                #  ner_columns = ['tui_description','cui_description', 'entities_description'],
                 ner_columns = ['tui','cui', 'entities'],
                 threshold_method='idf',
                 threshold_val=0
                 ):
        super().__init__(chemical_property_columns, embedding_columns, ner_columns, threshold_method, threshold_val)

        # self.embedding_columns = embedding_columns
        # self.columns = columns

        self.drugbank_ids = drugbank_ids

        zip_helper = ZipHelper()
        # zip_helper.extract(input_path=str(HERE.joinpath('drugbank_db.zip')), output_path=str(HERE))
        zip_helper.extract(input_path=str(HERE), output_path=str(HERE))
        # kwargs = {'index_path': str(HERE.joinpath('indexes'))}

        # db = HERE.joinpath('event.db')
        db = HERE.joinpath('drugbank.db')
        conn = create_connection(db)
        self.drugs_df = self.__select_all_drugs_as_dataframe__(conn)
        # dataframe'de olan ilaçlar arasındaki etkileşimleri bulmak için
        # self.drugbank_ids = self.drugs_df['id'].to_list()  ???
        self.ddis_df = self.__select_all_events__(conn)

        # self.index_path = kwargs.get('index_path')
        self.index_path = index_path

    def __select_all_events__(self, conn):
        param = tuple(self.drugbank_ids)
        cur = conn.cursor()
        query = f'''
            select
                _Interactions."index",
                drug_1_id,
                drug_1,
                drug_2_id,
                drug_2,
                mechanism_action, 
                interaction, 
                masked_interaction
            from _Interactions '''
        if len(self.drugbank_ids) > 0:
            query = query + \
                (f''' where drug_1_id in {format(param)} and drug_2_id in {format(param)}''')

        cur.execute(query)

        rows = cur.fetchall()

        headers = ['index', 'id1', 'name1', 'id2', 'name2',
                   'event_category', 'interaction', 'masked_interaction']
        df = pd.DataFrame(columns=headers, data=rows)
        return df

    # TODO tuis_description, entities_description, belli bir eşik değeri altında olanı ignore etmek lazım
    def __select_all_drugs_as_dataframe__(self, conn):
        param = tuple(self.drugbank_ids)
        query = f'''
            select 
            _Drugs."index",
            drugbank_id,
            _Drugs.name,
            description,
            synthesis_reference,
            indication,
            pharmacodynamics,
            mechanism_of_action,
            toxicity,
            metabolism,
            absorption,
            half_life,
            protein_binding,
            route_of_elimination,
            volume_of_distribution,
            clearance,
            smiles,
            smiles_morgan_fingerprint,
            enzymes_polypeptides,
            targets_polypeptides,
            pathways,
            tuis_description,
            cuis_description,
            entities_description
                    
            from _Drugs '''

        if len(self.drugbank_ids) > 0:
            query = query + f'''where 
                drugbank_id in {format(param)} and
                targets_polypeptides is not null and 
                enzymes_polypeptides is not null and 
                pathways is not null and 
                smiles_morgan_fingerprint is not null'''
        cur = conn.cursor()
        cur.execute(query)

        # pathway is absent

        rows = cur.fetchall()
        headers = ['index', 'id', 'name', 'description', 'synthesis_reference', 'indication', 'pharmacodynamics', 'mechanism_of_action', 'toxicity', 'metabolism', 'absorption', 'half_life',
                   'protein_binding', 'route_of_elimination', 'volume_of_distribution', 'clearance', 'smiles_notation', 'smile', 'enzyme', 'target', 'pathway',
                   'tui_description', 'cui_description', 'entities_description']
        df = pd.DataFrame(columns=headers, data=rows)
        df['smile'] = df['smile'].apply(lambda x:
                                        np.fromstring(
                                            x.replace(
                                                '\n', '')
                                            .replace('[', '')
                                            .replace(']', '')
                                            .replace('  ', ' '), sep=','))
        df['enzyme'] = df['enzyme'].apply(
            lambda x: x.split('|') if x is not None else [])
        df['target'] = df['target'].apply(
            lambda x: x.split('|') if x is not None else [])
        df['pathway'] = df['pathway'].apply(
            lambda x: x.split('|') if x is not None else [])
        df['tui_description'] = df['tui_description'].apply(
            lambda x: x.split('|') if x is not None else [])
        df['cui_description'] = df['cui_description'].apply(
            lambda x: x.split('|') if x is not None else [])
        df['entities_description'] = df['entities_description'].apply(
            lambda x: x.split('|') if x is not None else [])
        return df
