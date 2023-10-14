GCOV=-fprofile-arcs -ftest-coverage
all: build

UNAME:=$(shell uname -s)
ifeq ($(UNAME),Linux)
	LIBS=-lcheck -lsubunit -lrt -lm -lpthread
	LEAKS_IN = valgrind --leak-check=full
endif 
ifeq ($(UNAME),Darwin)
	LIBS=-lcheck -lm
	LEAKS_IN = leaks -atExit --
endif

install:
	pip3 install -r requirements.txt
	sudo apt install libgl1
	gcc -dynamiclib a.c calc.c -o main.dylib
	mkdir ../calculator 
	mkdir ../calculator/build 
	cp calculator.sh ../calculator/
	make clean

uninstall:
	rm -rf ../calculator 

build: clean
	gcc -dynamiclib a.c calc.c -lm -o main.dylib 
	python3 main.py

test:
	gcc -g test.c $(LIBS) -o test 
	./test

gcov_report:
	gcc $(CFLAGS) $(GCOV) test.c $(LIBS)  -o GcovReport
	./GcovReport
	lcov -t "GcovReport" -o GcovReport.info -c -d .
	genhtml -o report GcovReport.info 

clean:
	rm -rf ./*.o ./*.a ./a.out ./GcovReport ./*.gcno ./*.gcda ./report ./*.info *.dylib
	rm -rf *.exe *.ddl expression.c expression c_execute test __pycache__

clang_format:
	cp ../materials/linters/.clang-format .
	clang-format -n *.c 

clang_formating:
	clang-format --style=google -i *.c 
