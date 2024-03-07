#!/bin/bash
if semgrep --config ~/Desktop/semgrep/semgrep_rules/ ~/Desktop/scm; then
    echo "Kudos! Happy coding, your code is safe."
    exit 0
else
    echo "Semgrep violations detected. Fix the issues before pushing."
    exit 1
fi
