from assertpy import assert_that
from tests.global_test_data import df_global
from data_quality_kit.check_column_match import check_column_match


def test_column_match():
    df1 = df_global[['match_column1']].copy()
    df2 = df_global[['match_column2']].copy()
    assert_that(check_column_match(df1, 'match_column1', df2, 'match_column2')).is_true()


def test_column_match_with_duplicates():
    df1 = df_global[['match_column1']].copy()
    df2 = df_global[['match_column_with_duplicates']].copy()
    assert_that(check_column_match(df1, 'match_column1', df2, 'match_column_with_duplicates')).is_true()


def test_column_no_match():
    df1 = df_global[['match_column1']].copy()
    df2 = df_global[['unique_ids']].copy()
    assert_that(check_column_match(df1, 'match_column1', df2, 'unique_ids')).is_false()


def test_invalid_column_first_df():
    error_msg = 'Error: The column "nonexistent" does not exist in the first DataFrame.'
    assert_that(check_column_match).raises(ValueError).when_called_with(
        df_global[['match_column1']], 'nonexistent', df_global[['match_column2']], 'match_column2'
    ).is_equal_to(error_msg)


def test_invalid_column_second_df():
    error_msg = 'Error: The column "nonexistent" does not exist in the second DataFrame.'
    assert_that(check_column_match).raises(ValueError).when_called_with(
        df_global[['match_column1']], 'match_column1', df_global[['match_column2']], 'nonexistent'
    ).is_equal_to(error_msg)
