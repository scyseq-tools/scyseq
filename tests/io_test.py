import json

import numpy as np

from scyseq.io import read_codix, write_codix
from scyseq.sequence import Alphabet, Sequence


def test_read_new_codix_returns_sequences_by_default(tmp_path):
    path = tmp_path / "new.cdx"
    path.write_text(
        json.dumps(
            {
                "version": "0.9",
                "code": {"codes": {"gaze": ["away", "face"]}, "sites": {"infant": ["gaze"]}},
                "data": {"infant": {"gaze": [0, 1, 1, 0]}},
            }
        )
    )

    data = read_codix(path)
    seq = data["infant"]["gaze"]

    np.testing.assert_array_equal(seq.ivals, np.array([0, 1, 1, 0]))
    assert seq.alphabet.svals == ("away", "face")


def test_read_new_codix_can_return_full_record(tmp_path):
    path = tmp_path / "new.cdx"
    path.write_text(
        json.dumps(
            {
                "version": "0.9",
                "code": {"codes": {"gaze": ["away", "face"]}, "sites": {"infant": ["gaze"]}},
                "data": {"infant": {"gaze": [0, 1]}},
            }
        )
    )

    record = read_codix(path, data_only=False)

    assert record["version"] == "0.9"
    assert isinstance(record["data"]["infant"]["gaze"], Sequence)


def test_read_old_codix_converts_dictionaries_to_alphabets(tmp_path):
    path = tmp_path / "old.cdx"
    path.write_text(
        json.dumps(
            {
                "data": {
                    "mother": {
                        "affect": {
                            "seq": [1, 0, 1],
                            "dico": {"0": "neutral", "1": "positive"},
                        }
                    }
                }
            }
        )
    )

    data = read_codix(path)
    seq = data["mother"]["affect"]

    np.testing.assert_array_equal(seq.ivals, np.array([1, 0, 1]))
    assert seq.alphabet.svals == ("neutral", "positive")


def test_write_codix_creates_readable_new_codix_file(tmp_path):
    path = tmp_path / "roundtrip.cdx"
    seq = Sequence([0, 1, 1, 0], Alphabet(["away", "face"]))

    write_codix(path, {"infant": [("gaze", seq)]})

    raw = json.loads(path.read_text())
    assert raw["version"] == "0.9"
    assert raw["code"]["codes"]["gaze"] == ["away", "face"]
    assert raw["data"]["infant"]["gaze"] == [0, 1, 1, 0]

    data = read_codix(path)
    np.testing.assert_array_equal(data["infant"]["gaze"].ivals, seq.ivals)
    assert data["infant"]["gaze"].alphabet == seq.alphabet
