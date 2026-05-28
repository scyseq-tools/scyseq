Introduction
============

Symbolic dynamics provides a mathematical framework for representing complex
systems as sequences of discrete symbols. As described by Marcus and Williams
[MaWi08]_:

    “Symbolic Dynamics is the study of shift spaces, which consist of infinite or
    bi-infinite sequences defined by a shift-invariant constraint on the
    finite-length sub-words. Mappings between two such spaces can be regarded as
    codes or encodings. Shift spaces are classified, up to various kinds of
    invertible encodings, by combinatorial, algebraic, topological and
    measure-theoretic invariants. The subject is intimately related to dynamical
    systems, ergodic theory, automata theory and information theory.”

This formal perspective highlights the richness of symbolic sequence analysis
and its connections to multiple domains. More recent overviews of symbolic
dynamics can be found in [HiAm23]_, while [Cai23]_ presents a Python package
focused on the theoretical foundations of the field.

**ScySeq** adopts a complementary approach. Rather than focusing primarily on
theoretical developments, it provides a practical and modular framework for
working with symbolic sequences in applied contexts. The package enables users
to construct, manipulate, analyze, and visualize sequences of symbols in a
consistent and extensible way.

The motivation for ScySeq arises in particular from behavioral research, where
observations (e.g., movement, vocalization, interaction states) are often coded
as discrete events over time. These coded observations can naturally be
represented as symbolic sequences and analyzed to quantify structure,
variability, complexity, and recurrence patterns.

An example of the use of *ScySeq* in a behavioral context is provided in
[DoPN22]_.




