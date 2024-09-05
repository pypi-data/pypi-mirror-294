from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.completeness import assert_that_dataframe_is_empty


def test_assert_that_dataframe_is_empty_over_df_empty():
    df_empty = df_global.iloc[0:0]
    assert_that(assert_that_dataframe_is_empty(df_empty)).is_true()


def test_assert_that_dataframe_is_empty_over_df_not_empty():
    assert_that(assert_that_dataframe_is_empty(df_global)).is_false()
