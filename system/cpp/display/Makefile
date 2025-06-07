CC = g++
CFLAGS = -Wall -O2 -I./src -fPIC -g 
LIBS = -lbcm2835
LDFLAGS = -shared

SRC = \
    src/st7735.cpp \
    src/font.cpp \
    src/display_init.cpp \
    src/list_menu/list_menu.cpp \
    src/keyboard/keyboard.cpp

LIB_NAME = libst7735.so

all: $(LIB_NAME)

$(LIB_NAME): $(SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -f $(LIB_NAME)
