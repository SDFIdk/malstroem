import pytest
from malstroem import vector

labeledfile = 'tests/data/labelled.tif'

cell_to_world = [
    ((0, 0),  (720000.0, 0.4, 0.0, 6193000.0, 0.0, -0.4), (720000.2, 6192999.8)),
    ((1, 10), (720000.0, 0.4, 0.0, 6193000.0, 0.0, -0.4), (720004.2, 6192999.4))
]


@pytest.mark.parametrize("cell_coord, geotransform, expected_world_coord", cell_to_world)
def test_transform(cell_coord, geotransform, expected_world_coord):
    wld = vector.transform_cell_to_world(cell_coord, geotransform)
    assert wld == expected_world_coord


def test_vectorize():
    result = list(vector.vectorize_labels_file(labeledfile, 'bspot_id'))
    assert len(result) == 113

