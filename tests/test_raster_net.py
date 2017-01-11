import json

import pytest
from malstroem.algorithms import net
from data.fixtures import flowdirdata, bspotdata, pourpointsdata


def test_next_downstream_label(flowdirdata, bspotdata):
    pour_points = [(1, 18), (5, 129), (7, 27), (7, 109), (9, 120), (12, 2), (17, 47), (33, 204), (12, 163), (14, 108),
                   (18, 1), (23, 77), (20, 158), (21, 230), (24, 128), (26, 114), (34, 225), (27, 32), (30, 28),
                   (44, 60)]
    downstreams = [None, None, 7, None, 2, 11, 13, 26, None, 4, None, 10, 9, 21, 2, 5, 21, 7, 18, 33]

    for i, pp in enumerate(pour_points):
        lbl, geom = net.next_downstream_label(flowdirdata, bspotdata, pp, background_label=0, geometry=True)
        downstreams.append(lbl)
        assert geom
        last_coord = geom[-1]
        if lbl is not None:
            assert bspotdata[last_coord[0], last_coord[1]] == lbl
        assert downstreams[i] == lbl


def test_geometric_pourpoint_network(bspotdata, flowdirdata, pourpointsdata):
    nodes = net.geometric_pourpoint_network(flowdirdata, bspotdata, pourpointsdata, background_label=0)

    assert len(nodes) == 117
    assert len(nodes) >= len(pourpointsdata)
    assert max([n['id'] for n in nodes]) >= len(pourpointsdata)
    assert sum([n['nodetype'] == 'junction' for n in nodes]) == 12

    nodes_index = {}
    for n in nodes:
        nid = n['id']
        assert nid not in nodes_index
        nodes_index[nid] = n

    for n in nodes:
        assert n['geometry'][0] == n['pix']
        down_id = n['downstream_id']
        if down_id:
            downstream_node = nodes_index[down_id]
            if downstream_node['nodetype'] == 'junction':
                # Last coord must match next node coord if next node is junction
                assert n['geometry'][-1] == downstream_node['pix'], "Node flow mismatch {} to {}".format(n, downstream_node)
