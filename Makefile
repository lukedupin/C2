
DEFINE = -DCPLUSPLUS
COMP_OPTS = 
LIBRARIES = -lm

BISON_OPTS = -v -t -d

OBJECTS = \
          build/parser.tab.o

COMP = g++

EXECUTABLE = c2

$(EXECUTABLE):	 main.cpp flex $(OBJECTS)
		$(COMP) $(DEFINE) $(COMP_OPTS) main.cpp lex.yy.c $(OBJECTS) $(LIBRARIES) -o $(EXECUTABLE)

flex:	scanner.lex bison
	flex $(FLEX_OPTS) scanner.lex

bison:	parser.y
	bison $(BISON_OPTS) parser.y

build/%.o:	%.cpp %.h
	$(COMP) $(DEFINE) $(COMP_OPTS) -c $*.cpp -o build/$*.o

build/parser.tab.o:	parser.tab.c parser.tab.h
	$(COMP) $(DEFINE) $(COMP_OPTS) -c parser.tab.c -o build/parser.tab.o

clean:
	-rm -f scanner.output scanner.tab.c parser.tab.h lex.yy.c build/*
	-rm -f $(EXECUTABLE)
