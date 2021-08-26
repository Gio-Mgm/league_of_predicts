from frontend.V3.src.classes import Match


class TestMatch:
    match = Match()

    def test_convert_kda(self):
        assert self.match.convert_kda('10/25/258') == ['10', '25', '258']

    def test_convert_golds(self):
        assert self.match.convert_golds('20.3k') == 20300

    def test_convert_timer(self):
        assert self.match.convert_timer('20:30') == 20.5
        assert self.match.convert_timer('20.5') == 20.5

    def test_is_valid(self):
        assert self.match.is_valid('kda', '10/25/258')
        assert not self.match.is_valid('kda', '/25/258')
        assert self.match.is_valid('timer', '10:30')
        assert not self.match.is_valid('timer', '10:68')
        assert self.match.is_valid('golds', '21.3k')
        assert not self.match.is_valid('golds', '21.3')
        assert self.match.is_valid('towers', '5')
        assert not self.match.is_valid('towers', '16')

    def test_get_attr(self):
        assert len(self.match.test_get_attr(self.match)) == 9

    def test_get_values(self):
        self.match.timer == 20.5
        assert self.match.get_values(self.match)[-1] == 20.5

    def test_set_attr(self):
        self.match.set_attr('timer', '10:30')
        assert self.match.timer == 10.5



atch = Match()
atch.timer = 42
print(Match.get_attr(atch))
print(Match.get_values(atch))
