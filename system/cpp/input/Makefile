CC = g++
CFLAGS = -Wall -O2 -I./src -fPIC -g 
LIBS = -lbcm2835
LDFLAGS = -shared

SRC = \
    src/buttons_input.cpp

LIB_NAME = libinput.so

all: $(LIB_NAME)

$(LIB_NAME): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -f $(LIB_NAME)
