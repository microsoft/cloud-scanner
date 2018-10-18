setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

remove_unnecessary_files(){
  find . -maxdepth 1 -type f -not \( -name '*.html' -or -name '*.js' -or -name '*.css' \) -delete
  find . -maxdepth 1 -type d -not \( -name ".git" -or -name "." -or -name "generated" -or -name "_static" \) -exec rm -irf {} \; 
}

commit_website_files() {
  git checkout -b gh-pages
  mv docs/build/html new-docs
  rm -rf docs
  mv new-docs docs
  cp -r docs/* .
  remove_unnecessary_files
  touch .nojekyll
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER [skip ci]"
}

upload_files() {
  git remote add origin-pages https://${GITHUB_TOKEN}@github.com/Microsoft/cloud-scanner.git > /dev/null 2>&1
  git push origin-pages gh-pages --force
}

make sphinx
setup_git
commit_website_files
upload_files