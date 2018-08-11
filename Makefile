all:
	make html
	make latex
	make pdf

html:
	mkdir -p build
	sphinx-build -M html  "." "build"

latex:
	mkdir -p build
	sphinx-build -M latex "." "build"

pdf:
	mkdir -p build/pdf/latex
	sphinx-build -M latexpdf "." "build/pdf"
	mv build/pdf/latex/etc_tech_ref.pdf build/pdf/
	rm -rf build/pdf/latex
