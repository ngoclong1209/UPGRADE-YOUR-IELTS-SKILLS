#!/bin/bash
set -e

echo "Pushing root files and small folders..."
git add Docs Tools *.html *.py *.js *.xlsx || true
git commit -m "Initial commit: Tools, Docs, Root files"
git push -u origin main

echo "Pushing Reading and Basic Listening..."
git add Reading_1232_Basic Reading_315_FullTest Reading_docx Listening_docx Listening_102_Basic || true
git commit -m "Add Reading and basic Listening materials"
git push

echo "Pushing Listening FullTest in chunks..."
count=0
for dir in Listening_204_FullTest/*; do
  if [ -d "$dir" ]; then
    git add "$dir"
    count=$((count+1))
    if [ $((count % 20)) -eq 0 ]; then
      echo "Committing chunk $count..."
      git commit -m "Add Listening_204_FullTest chunk $count"
      git push
    fi
  fi
done

# Commit any remaining
git add Listening_204_FullTest || true
git commit -m "Add remaining Listening_204_FullTest" || true
git push || true

echo "Done!"
