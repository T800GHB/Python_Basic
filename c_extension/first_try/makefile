all: math_opt.so

math_opt.so: math_opt.o
	g++ -shared -o math_opt.so math_opt.o
math_opt.o:
	g++ -fpic -c -I /home/andrew/anaconda3/include/python3.6m/ math_opt.cpp
clean:
	rm -f math_opt.o math_opt.so
