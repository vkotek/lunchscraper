import os, sys

try:
    import controller, cli, lunchscraper
except:
    from lunchscraper import controller, cli, lunchscraper

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
