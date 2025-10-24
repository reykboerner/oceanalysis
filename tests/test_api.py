import io
import sys

import oceanalysis


def capture_print(func, *args, **kwargs):
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        func(*args, **kwargs)
    finally:
        sys.stdout = old
    return buf.getvalue()


def test_model_mask_plot():
    model = oceanalysis.OceanModel(name="test-model")
    out = capture_print(model.mask.plot)
    assert "Plotting mask for model=" in out


def test_data_var_summary_and_compute():
    data = oceanalysis.OceanData(source="test-data")
    out_var = capture_print(data.var.summary)
    assert "Variables summary for data" in out_var
    out_comp = capture_print(data.compute.run, "median")
    assert "Running compute operation" in out_comp
