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
	mv docs/* . && \
	rm -rf docs && \
	touch .nojekyll && \
	git add . && \
	git commit -m "Updated generated Sphinx documentation"mit -m "Updated generated Sphinx documentation"
