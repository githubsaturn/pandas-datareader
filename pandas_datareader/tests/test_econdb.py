import numpy as np
import pandas as pd
import pandas.util.testing as tm
import pandas_datareader.data as web


class TestEcondb(object):

    def test_get_cdh_e_fos(self):
        # EUROSTAT
        # Employed doctorate holders in non managerial and non professional
        # occupations by fields of science (%)
        df = web.DataReader(
            'dataset=CDH_E_FOS&GEO=NO,PL,PT,RU&FOS07=FOS1&Y_GRAD=TOTAL',
            'econdb',
            start=pd.Timestamp('2005-01-01'),
            end=pd.Timestamp('2010-01-01'))
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 4)

        df = df['Annual']['Natural sciences'][
                ['Norway', 'Poland', 'Portugal', 'Russia']]

        exp_col = pd.MultiIndex.from_product(
            [['Norway', 'Poland', 'Portugal', 'Russia'],
             ['Total'], ['Percentage']],
            names=['Geopolitical entity (reporting)',
                   'Year of graduation', 'Unit of measure'])
        exp_idx = pd.DatetimeIndex(['2006-01-01', '2009-01-01'],
                                   name='TIME_PERIOD')

        values = np.array([[25.49, np.nan, 39.05, np.nan],
                           [20.38, 25.1, 27.77, 38.1]])
        expected = pd.DataFrame(values, index=exp_idx, columns=exp_col)
        tm.assert_frame_equal(df, expected)

    def test_get_tourism(self):
        # OECD
        # TOURISM_INBOUND

        df = web.DataReader(
            'dataset=OE_TOURISM_INBOUND&COUNTRY=JPN,USA&'
            'VARIABLE=INB_ARRIVALS_TOTAL', 'econdb',
            start=pd.Timestamp('2008-01-01'), end=pd.Timestamp('2012-01-01'))
        df = df.astype(np.float)
        jp = np.array([8351000, 6790000, 8611000, 6219000,
                       8368000], dtype=float)
        us = np.array([175702309, 160507417, 164079732, 167600277,
                       171320408], dtype=float)
        index = pd.date_range('2008-01-01', '2012-01-01', freq='AS',
                              name='TIME_PERIOD')
        for label, values in [('Japan', jp), ('United States', us)]:
            expected = pd.Series(values, index=index,
                                 name='Total international arrivals')
            tm.assert_series_equal(df[label]['Total international arrivals'],
                                   expected)

    def test_bls(self):
        # BLS
        # CPI
        df = web.DataReader(
            'ticker=BLS_CU.CUSR0000SA0.M.US', 'econdb',
            start=pd.Timestamp('2010-01-01'), end=pd.Timestamp('2013-01-27'))

        assert df.loc['2010-05-01'][0] == 217.3
