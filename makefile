CC=g++
CC_GCC=g++-11
CC_CLANG=clang++-12
#CC=clang++
CPPSTD=-std=c++20 # -fconcepts-diagnostics-depth=2  # -Wfatal-errors
#CPPSTD=--std=c++17 -fconcepts -Wfatal-errors

all: optframe_lib demo_local

optframe_lib:
	# mkdir -p build/
	# -Wextra
	@echo "IMPORTANT: Remember to point src/optframe-src to optframe project /include directory"
	@echo "EXAMPLE: ln -s  my/full/optframe/include  src/optframe-src"
	#
	@echo "BUILD WITH ${CC_GCC} (PART 1/2)"
	$(CC_GCC) $(CPPSTD) -g -Isrc/optframe-src/include -Wall -pedantic -Ofast --shared optframe/optframe_lib.cpp -o optframe/optframe_lib.so -fPIC
	#
	@echo "BUILD WITH ${CC_CLANG} (PART 2/2)"
	$(CC_CLANG) $(CPPSTD) -g -Isrc/optframe-src/include -Wall -pedantic -Ofast --shared optframe/optframe_lib.cpp -o optframe/optframe_lib.so -fPIC
	#
	#readelf -s build/optframe_lib.so | grep fcore

publish_test:
	rm -f dist/*
	python -m build
	rm -f dist/*.whl
	twine check dist/*
	twine upload -r testpypi dist/* --verbose
	


demo_local: optframe/optframe_lib.so
	# valgrind --leak-check=full python3 demo/demo_kp.py 
	python3 demo/demo_kp.py 

.PHONY: docs

docs:
	cd docs && make clean && make html


test:   #install
	# (cd demo/ && python3 demo_pyfcore.py)
	(cd tests/ && python3 test_pkg_engine_kp.py)
	

install:
	#pip install  --global-option=build_ext --global-option="-I$(pwd)/../optframe/include" .
	rm -rf ./optframe-git/
	pip install .

clean:
	rm -f optframe/*.so
