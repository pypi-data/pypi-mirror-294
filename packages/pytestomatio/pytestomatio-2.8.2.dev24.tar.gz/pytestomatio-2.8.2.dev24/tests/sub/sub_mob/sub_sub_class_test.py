from pytest import mark


class TestClassSubSub:

    def test_one_pass_sub(self):
        x = 'this'
        assert 'h' in x

    def test_two_fail_sub(self):
        x = 'hello'
        assert hasattr(x, 'check')

    @mark.skip
    def test_three_skip_sub(self, dummy_fixture):
        x = 'hello'
        assert hasattr(x, 'check')
