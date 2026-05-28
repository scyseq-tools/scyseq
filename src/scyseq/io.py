import json
from datetime import datetime

from scyseq import sequence as S


def read_codix(fname, data_only=True):
    """
    Reads data file from the codix encoder of the codix software suite for
    behavioral studies.

    returns in all cases a dictionary with data['site']['code'] = Sequence

    """
    with open(fname) as datafile:
        record = json.load(datafile)

    if "version" in record:
        # new codix suite format
        retval = __parse_new_codix__(record)
    else:
        # old codix format
        retval = __parse_old_codix__(record)

    if data_only:
        return retval["data"]
    else:
        return retval


def write_codix(fname, seqs, info=None):

    __version__ = "0.9"

    container = {
        "history": [],  # [(date, observer, comment), ...]
        "media": "",  # path for the media file
        "code": {},  # dictionary taken from the code file
        "times": [],  # sample times (in ms) taken from the player
        "comments": [],  # sample comments taken from codingframe
        "data": {},
        "version": __version__,
    }  # data
    # seqs = {site1: {cod1: sequence, cod2: sequence...}, site2: {...} ...}

    tmpcodes = {"codes": {}, "sites": {}}
    tmpdata = {}

    for site in seqs:
        if site not in tmpcodes["sites"]:
            tmpcodes["sites"].update({site: []})
        if site not in tmpdata:
            tmpdata.update({site: {}})
        for code, seq in seqs[site]:
            if code not in tmpcodes["codes"]:
                alpha = list(seq.alphabet.svals)
                tmpcodes["codes"].update({code: alpha})
            if code not in tmpdata[site]:
                tmpdata[site].update({code: seq.ivals.tolist()})

    container["code"] = tmpcodes
    container["data"] = tmpdata
    date = datetime.now().strftime("%c")
    comment = ""
    container["history"].append((date, "cdx-analyzer", comment))

    with open(fname, "w") as datafile:
        json.dump(container, datafile)


def __parse_old_codix__(record):

    data = record["data"]
    new_data = {}

    for channel in data:
        new_data[channel] = {}

        for coding in data[channel]:
            tmp_seq = data[channel][coding]["seq"]
            tmp_dico = data[channel][coding]["dico"]

            retval = [""] * len(tmp_dico)
            for k, v in tmp_dico.items():
                retval[int(k)] = str(v)
            alphabet = S.Alphabet(retval)

            new_data[channel][coding] = S.Sequence(tmp_seq, alphabet)

    record["data"] = new_data

    return record


def __parse_new_codix__(record):

    code = record["code"]
    data = record["data"]

    alphabets = {k: S.Alphabet(v) for k, v in code["codes"].items()}

    new_data = {}
    for site in data:
        new_data[site] = {}
        for cod in data[site]:
            tmp_seq = data[site][cod]
            alpha = alphabets[cod]
            new_data[site][cod] = S.Sequence(tmp_seq, alpha)

    record["data"] = new_data

    return record
