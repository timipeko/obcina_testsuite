# obcina_testsuite

Web crawler for municipality blog website. Checks website navbar for broken links. 

Running instructions:
1. Provide a url.txt file. Ask author for example urls. 
2. Install dependencies with `pipenv install`.
3. Run with `python functional_tests.py`.

Note: the excess sys.exit() calls and main method try-except are to ensure proper demo execution on unknown host machines. The unittest runner fails clean with a normal main() call under typical circumstances, sys.exit() can be replaced with the TestCase.fail() method. 
