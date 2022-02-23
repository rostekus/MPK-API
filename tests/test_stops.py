import pytest
import stops.stops as stops



@pytest.mark.parametrize("address, number, expected_result", [
    ("", "1332", (0,0)),
    ("","", (0,0)),
    ("f435rfds" , "fgegffd", (0,0)),
    # ("Piotrkowska pl. Niepodległości","0686",(51.7402595, 19.4626091)),
    # ("Aleksandrowska Lechicka" "0022", (51.8040076, 19.3618336)),
])
def test_get_location(address, number,expected_result):
        assert stops.get_location(address, number) == expected_result

