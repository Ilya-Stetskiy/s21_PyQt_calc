

GCOV=-fprofile-arcs -ftest-coverage
all: install build

UNAME:=$(shell uname -s)
ifeq ($(UNAME),Linux)
	LIBS=-lcheck -lsubunit -lrt -lm -lpthread
	LEAKS_IN = valgrind --leak-check=full
endif 
ifeq ($(UNAME),Darwin)
	LIBS=-lcheck -lm
	LEAKS_IN = leaks -atExit --
endif

install: uninstall
	pip3 install -r requirements.txt
	gcc -dynamiclib a.c calc.c -o main.dylib
	mkdir ../calculator 
	mkdir ../calculator/build 
	cp calculator.sh ../calculator/
	make clean

uninstall:
	rm -rf ../calculator 
dist:
	gcc -dynamiclib a.c calc.c -lm -o main.dylib 
dvi:
	open dvi.txt
build: clean
	gcc -dynamiclib a.c calc.c -lm -o main.dylib 
	python3 main.py

test: clean
	gcc -g test.c $(LIBS) -o test 
	./test

gcov_report:
	gcc $(CFLAGS) $(GCOV) test.c $(LIBS)  -o GcovReport
	./GcovReport
	lcov -t "GcovReport" -o GcovReport.info -c -d .
	genhtml -o report GcovReport.info 
	open ./report/index.html

clean:
	rm -rf ./*.o ./*.a ./a.out ./GcovReport ./*.gcno ./*.gcda ./report ./*.info *.dylib
	rm -rf ./main.dylib-*
	rm -rf *.exe *.ddl expression.c expression c_execute test __pycache__

check:
	cp ../materials/linters/.clang-format .
	clang-format -n *.c 

clang_formating:
	clang-format --style=google -i *.c 

make_more_space:
	rm -rf ~/Library/Caches/*
	rm -rf ~/Library/42_cache
	rm -rf ~/Library/Application\ Support/Slack/Service\ Worker/CacheStorage/
	rm -rf ~/Library/Application\ Support/Slack/Cache/
	rm -rf ~/Library/Application\ Support/Slack/Code\ Cache/
	rm -rf ~/Library/Application\ Code/Cache/*
	rm -rf ~/Library/Application\ Code/CachedData/*
	rm -rfv ~/Library/Caches/*
	rm -rfv ~/Library/Application\ Support/Slack/Cache/*
	rm -rfv ~/Library/Application\ Support/Slack/Service\ Worker/CacheStorage/*
	rm -rfv ~/Library/Group\ Containers/6N38VWS5BX.ru.keepcoder.Telegram/account-570841890615083515/postbox/*
	rm -rfv ~/Library/Application\ Support/Code/Cache
	rm -rfv ~/Library/Application\ Support/Code/CachedData
	rm -rfv ~/Library/Application\ Support/Code/CachedExtension
	rm -rfv ~/Library/Application\ Support/Code/CachedExtensions
	rm -rfv ~/Library/Application\ Support/Code/CachedExtensionVSIXs
	rm -rfv ~/Library/Application\ Support/Code/Code\ Cache
	rm -rfv ~/Library/Application\ Support/Slack/Cache
	rm -rfv ~/Library/Application\ Support/Slack/Code\ Cache
	rm -rfv ~/Library/Application\ Support/Slack/Service\ Worker/CacheStorage
	rm -rfv ~/Library/Application\ Support/Code/User/workspaceStorage