import json

import numpy as np

from scyseq.generator import generate
from scyseq.io import read_codix, write_codix
from scyseq.sequence import Alphabet, Sequence


def test_read_new_codix_returns_sequences_by_default(tmp_path):
    path = tmp_path / "new.cdx"
    path.write_text(
        json.dumps(
            {
                "version": "0.9",
                "code": {
                    "codes": {"gaze": ["away", "face"]},
                    "sites": {"infant": ["gaze"]},
                },
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
                "code": {
                    "codes": {"gaze": ["away", "face"]},
                    "sites": {"infant": ["gaze"]},
                },
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


def assert_roundtrip_matches(original, roundtrip):
    assert len(roundtrip) == len(original)
    assert roundtrip.alphabet == original.alphabet
    np.testing.assert_array_equal(roundtrip.ivals, original.ivals)


def test_generated_sequences_can_roundtrip_through_codix(tmp_path):
    path = tmp_path / "generated_methods.cdx"

    np.random.seed(123)
    markov_matrix = np.array(
        [
            [0.85, 0.15],
            [0.20, 0.80],
        ]
    )

    generated = {
        "uniform_state": Sequence(
            generate("uniform", 20, 3).ivals,
            Alphabet(["low", "mid", "high"]),
        ),
        "markov_state": Sequence(
            generate("markov", 20, 2, markov_matrix, 1).ivals,
            Alphabet(["rest", "active"]),
        ),
        "binary_logistic_state": Sequence(
            generate("binary_logistic", 20, 2, 4.0, 0.2).ivals,
            Alphabet(["below_threshold", "above_threshold"]),
        ),
    }

    write_codix(path, {"synthetic": list(generated.items())})

    roundtrip = read_codix(path)["synthetic"]

    assert set(roundtrip) == set(generated)
    for code, sequence in generated.items():
        assert_roundtrip_matches(sequence, roundtrip[code])
