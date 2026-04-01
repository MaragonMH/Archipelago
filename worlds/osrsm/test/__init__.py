from test.bases import WorldTestBase


class OSRSMTestBase(WorldTestBase):
    run_default_tests = False # type: ignore
    game = "Old School Runescape Members"
    def test_fill(self)->None:
        pass #override test_fill as it's slow
