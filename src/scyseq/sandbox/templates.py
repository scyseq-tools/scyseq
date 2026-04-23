#!/usr/bin/env python
#-*- coding:Utf-8 -*-

from string import Template

def single_substitute(result):
    return single.safe_substitute(res)

single = Template("""
Properties of the sequence
==========================

- length of the sequence: ${N} 

- Alphabet size: ${k}

- Meaning of symbols: ${d}

- *Serie is not printed* Should I plot it?

Visited states
==============

::
   
   ${visit}

Entropies
=========

- Shannon: ${shannon}

- Topologic: ${topologic}

Lempel-Ziv "complexities"
=========================

- lzn = h / ln(k): ${lzn}

- lzk = lzn * ln(k) = h: ${lzk}

- Effective LZ complexity (h / ln(v)): ${lzv}

- p-value (${nb_sur} surrogates): ${plz}
    
Effective_complexity
====================

.. warning::
   
   Do not use effective complexity since it's not stable

- Effective complexity: ${ec}

Recurrence Plot
===============

.. warning::

   Should print the graph...

""")
        
# rp = RP.recurrence_plot((seq,)))
    
pair = Template("""
""")
