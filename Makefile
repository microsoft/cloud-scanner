sphinx:
	cd docs && \
	make clean && \
	sphinx-apidoc -f -o source/generated ../cloud_scanner && \
	make html

ghpages:
	-git checkout gh-pages && \
	mv docs/build/html new-docs && \
	rm -rf docs && \
	mv new-docs docs && \
	git add -u && \
	git add -A && \
	git commit -m "Updated generated Sphinx documentation"