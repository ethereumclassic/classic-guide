#!/usr/bin/env python3

# --- general ------------------------------------------------------------------

project       = "Ethereum Classic Technical Reference"
author        = "Christian Seberino"
copyright     = "2018 " + author
version       = "0.1"
release       = version
master_doc    = "index"
source_suffix = ".rst"
extensions    = ["sphinx.ext.autodoc",
                 "sphinx.ext.doctest",
                 "sphinx.ext.intersphinx",
                 "sphinx.ext.todo",
                 "sphinx.ext.coverage",
                 "sphinx.ext.mathjax",
                 "sphinx.ext.ifconfig",
                 "sphinx.ext.viewcode",
                 "sphinx.ext.githubpages"]

# --- HTML ---------------------------------------------------------------------

html_sidebars    = {"*" : ["searchbox.html", "relations.html"]}
html_static_path = ["static"]

# --- Latex --------------------------------------------------------------------

latex_engine              = 'xelatex'
latex_toplevel_sectioning = "part"
latex_documents           = [(master_doc,
                              "etc_tech_ref.tex",
                              project,
                              author,
                              "howto")]
