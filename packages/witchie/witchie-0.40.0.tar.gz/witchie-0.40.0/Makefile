# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
#
# SPDX-License-Identifier: GPL-3.0-only

.PHONY: clean publish test docs

dist :
	python setup.py sdist --formats=gztar,zip
	python setup.py bdist_wheel --python-tag=py3

publish :
	twine upload dist/*.tar.gz dist/*.whl

test:
	pytest -v
	flake8
	vermin witchie

coverage:
	coverage erase
	coverage run
	coverage html
	coverage report

clean :
	find . -name "*pyc" | xargs rm -rf $1
	rm -rf build dist MANIFEST htmlcov witchie*.tar.gz

changelog:
	./scripts/generate_changelog > CHANGELOG.md
	cp CHANGELOG.md docs/changelog.md

docs: changelog
	mdbook build

docs-serve:
	mdbook serve

docs-deploy: docs
	rsync --archive --compress --delete --stats book/ bezdomni:web/witchie
