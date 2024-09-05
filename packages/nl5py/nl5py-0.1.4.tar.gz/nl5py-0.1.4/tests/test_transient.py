import pytest
from nl5py import Schematic

import pytest
import os

schematic_file = os.path.join(os.path.dirname(__file__), "rc.nl5")
schematic = Schematic(schematic_file)


def test_add_remove_traces():
    schematic.add_trace("C1", "V")
    schematic.add_trace("C1", "I")
    schematic.add_trace("C1", "P")
    schematic.add_trace("V(C1)*I(C1)")

    traces = schematic.get_trace_names()
    assert "V(C1)" in traces
    assert "I(C1)" in traces
    assert "P(C1)" in traces
    assert "V(C1)*I(C1)" in traces

    schematic.delete_trace("V(C1)")
    traces = schematic.get_trace_names()
    assert "V(C1)" not in traces

    schematic.clear_traces()
    traces = schematic.get_trace_names()
    assert not traces


def test_simulation():
    schematic.set_value("V1", 1)
    schematic.set_value("C1", 1)
    schematic.set_value("R1", 1)
    schematic.set_value("C1.IC", 0)
    schematic.add_trace("V(C1)")
    schematic.simulate_transient(screen=1, step=1e-3)
    data = schematic.get_data()
    print(data["V(C1)"].iloc[0])
    assert data["V(C1)"].iloc[0] < 0.1
    assert data["V(C1)"].iloc[-1] < 0.634
    assert data["V(C1)"].iloc[-1] > 0.631
