from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.completeness.assert_that_dataframe_is_empty import df_is_empty


def test_df_is_empty():
    df_empty = df_global.iloc[0:0]
    assert_that(df_is_empty(df_empty)).is_true()


def test_df_is_not_empty():
    assert_that(df_is_empty(df_global)).is_false()
