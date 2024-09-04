from permanence import ObjectPermanence, Arty, ScopeNamespace
from permanence.tag_type import Tagged
from permanence.chunks import (
    LocalChunk,
    MutableLocalChunk,
    ChunkCollection,
    TaggedLocalArtifact,
)
from permanence.artifact import TableArtifact

import pandas as pd

import asyncio
import time


def test_chunk_append():
    df = pd.DataFrame({"x": [1, 2, 3], "z": ["a", "b", "d"]})

    ch = MutableLocalChunk.new()
    af_bin, af = Arty.Table.Foo.new(df)
    ch.append(af_bin, TaggedLocalArtifact(df, af, Tagged({}), 0.0))

    chc = ChunkCollection([ch])
    assert not chc.query().empty


def test_chunk_roundtrip():
    space = ScopeNamespace("just-for-testing_chunks")
    pr = ObjectPermanence(space)

    @pr.new_scope
    class Params(pr.Scope):
        n: int

    df_a = pd.DataFrame({"x": [1, 2, 3], "z": ["a", "b", "d"]})
    df_b = pd.DataFrame({"q": [1, 2, 3], "m": ["a", "b", "d"]})

    with pr.context(Params(1001)):
        something_af = pr.logged(Arty.Table.Something, df_a)
        assert isinstance(something_af, TableArtifact)
        print(something_af.data_hash)

        assert pr.query(values=Arty.Table.Something).only().artifact == something_af

        with pr.using(something_af) as _:
            pr.logged(Arty.Table.SomethingElse, df_b)

    metric_log = {"metric:accuracy": 1000000000.0}

    with pr.context(Params(1002)):
        # Test all artifact types
        pr.logged(Arty.Table.Something, df_a)
        pr.logged(Arty.JSON.MetricsOrIDK, metric_log)

    new_doc_id = asyncio.run(pr.chunks().into_document())  # Upload

    pr_alt = ObjectPermanence(space)

    assert pr_alt.query().empty

    read_chunks = asyncio.run(
        ChunkCollection.document_to_local_chunks(pr_alt.scope_namespace, new_doc_id)
    )
    assert len(read_chunks.query()) == 4

    # Test chunk API and behaviour on loaded contents

    with pr_alt.overlayed(read_chunks):
        assert len(pr_alt.query()) == 4

        # Map hash -> artifact
        assert pr_alt.checkout(something_af.data_hash) == something_af

        with pr_alt.context(something_af):
            matched = pr_alt.query().only()
            assert matched.artifact.scope_name() == "SomethingElse"
            assert isinstance(matched.artifact, TableArtifact)
            assert (matched.load().to_pandas() == df_b).all().all()

        # Test log time was within 5 seconds ago
        assert (
            0
            < time.time() - pr_alt.query(values=Arty.JSON.MetricsOrIDK).only().logged_at
            < 5
        )

        assert pr_alt.query(values=Arty.JSON.MetricsOrIDK).only().load() == metric_log

        # Map artifact -> contents
        with pr_alt.using(something_af) as something:
            assert (something.to_pandas() == df_a).all().all()

    assert pr_alt.query().empty
