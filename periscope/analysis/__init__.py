"""Periscope-derived analysis library.

Every function here reads a canonical dataset (periscope.datasets.canonicalize)
and returns a new, separate structure -- it never writes derived values back
into the canonical dataset, and never recomputes a NeoMundi signal
differently. See docs/METRIC_BOUNDARIES.md.
"""
