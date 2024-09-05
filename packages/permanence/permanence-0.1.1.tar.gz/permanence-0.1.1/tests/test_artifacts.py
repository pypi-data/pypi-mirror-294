from permanence import Arty
from permanence.artifact import Artifact

import pyarrow as pa
import pandas as pd

from io import BytesIO


def test_artifact_types():
    sample_artifact_contents = {
        "JSON": {"x": 11, "y": [5, 6, 7]},
        "Table": pa.Table.from_pandas(
            pd.DataFrame({"x": ["a", "b", "c"], "y": [0.0, 10.0, 100.0]})
        ),
        "Binary": b"asdfqwertblob",
    }

    for af_type_name, af_content in sample_artifact_contents.items():
        af_type = getattr(Arty, af_type_name)
        af_bin, artifact = af_type.SomeJSON.new(af_content)
        assert isinstance(artifact, Artifact)
        assert artifact.reconstruct(af_bin) == af_content

    # Some artifacts accept additional input types:

    binary_file = BytesIO(b"aaaaaaaaaaaaaAaAaaAaAAAA")
    binary_data, binary_af = Arty.Binary.AAA.new(binary_file)
    assert binary_file.closed
    assert binary_af.reconstruct(binary_data) == b"aaaaaaaaaaaaaAaAaaAaAAAA"
