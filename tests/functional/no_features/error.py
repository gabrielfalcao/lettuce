
# some modules have problems when loaded directly with __import__
# rather than being imported via their absolute names (e.g. django models)
# see issue #391
raise RuntimeError("please do not import this file directly")
