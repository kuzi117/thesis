PREFIX=thesis
SUBFILES=$(wildcard tex/*)
FIGURES=$(wildcard tex/figures/*)
BIB=refs.bib
LATEX=pdflatex -halt-on-error
BIBTEX=bibtex

all: $(PREFIX).pdf

pdf: $(PREFIX).pdf

print:
	@echo $(FIGURES)

%.pdf: %.tex $(SUBFILES) $(BIB) $(FIGURES)
	$(LATEX)	$(PREFIX)
	$(BIBTEX)	$(PREFIX)
	$(LATEX)	$(PREFIX)
	$(BIBTEX)	$(PREFIX)
	$(LATEX)	$(PREFIX)

clean:
	$(RM) *.log *.dvi *.toc *.lot *.lof *.aux *.bbl *.blg *.out *.pdf *-blx.bib *.run.xml
