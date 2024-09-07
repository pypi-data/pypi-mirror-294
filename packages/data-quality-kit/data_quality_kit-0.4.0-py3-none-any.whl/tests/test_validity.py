from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.validity import assert_that_there_are_not_nulls


def test_assert_that_there_are_not_nulls_over_nulls_present():
    assert_that(assert_that_there_are_not_nulls(df_global, 'column2')).is_true()


def test_assert_that_there_are_not_nulls_over_no_nulls():
    assert_that(assert_that_there_are_not_nulls(df_global, 'column1')).is_false()
    assert_that(assert_that_there_are_not_nulls(df_global, 'column3')).is_false()


def test_assert_that_there_are_not_nulls_over_invalid_column_type():
    error_msg = 'Error: Field name must be a string.'
    assert_that(assert_that_there_are_not_nulls).raises(TypeError).when_called_with(
        df_global, 123
    ).is_equal_to(error_msg)


def test_assert_that_there_are_not_nulls_over_invalid_column_name():
    error_msg = 'Error: Field "nonexistent" not in DataFrame.'
    assert_that(assert_that_there_are_not_nulls).raises(ValueError).when_called_with(
        df_global, "nonexistent"
    ).is_equal_to(error_msg)
