# Some systems apparently distinguish between shell 
# variables and environment variables. The latter are
# visible to the make utility, the former apparently not,
# so we need to set them if they are not defined yet

# ===============================================================================
# COMPILATION PREFERENCES
# ===============================================================================
# CCACHE: if set to ccache, use ccache to speed up compilation
# OPTI:   optimization level
# PROF:   profiler switches 

.DEFAULT_GOAL = all
.SECONDARY:
CCACHE  = ccache
OPTI    = 3
EXE_TAG = exe
# PROF = -g -pg

# ===============================================================================

.DEFAULT_TARGET = all

# ===============================================================================
# COMPILATION 'LOCALIZATION'
HOST     ?= $(shell hostname)
HOSTTYPE ?= $(shell uname -m)

MTSPELLTOP = ..
INCLUDES   = $(addprefix -I,${MTSPELLTOP}/include)
LIBDIRS    = $(addprefix -L,${MTSPELLTOP}/lib)
WDIR       = build/${HOSTTYPE}/${OPTI}
CXXFLAGS   = ${PROF} -ggdb -Wall -O${OPTI} ${INCLUDES} ${LIBDIRS} 
#CXXFLAGS  += -static -pthread
BINDIR     = bin
LIBS = $(addprefix -l,boost_iostreams icuuc icuio icui18n cmph dl)
ifeq "$(OPTI)" "0"
BINPREF = debug.
else
BINPREF = 
endif

clean:
	rm -f ${WDIR}/*.o ${WDIR}/*.d

DEP     = $(prereqs:.o=.d)
OBJ     = $(patsubst %.cc,%.o,$(wildcard $(patsubst %.h,%.cc,$(wildcard *.h))))
prereqs = $(addprefix ${WDIR}/, $(OBJ))

${BINDIR}/${BINPREF}%: ${WDIR}/%.exe
	cp $< $@

${WDIR}/%.exe: %.o $(prereqs) $(wildcard *.h)
	@echo COMPILING $@
	@echo PREREQS $(prereqs)
	mkdir -p ${WDIR} ${BINDIR}
	$(CXX) $(CXXFLAGS) -o $@ $(prereqs) $< ${LIBS} 

${WDIR}/%.o : %.cc
	mkdir -p ${WDIR}
	${CXX} ${CXXFLAGS} -MD -MP -c $(abspath $<) -o $@ 

cmph.demo: file_adapter_ex2.c
	${CXX} ${CXXFLAGS} -MD -MP file_adapter_ex2.c -o $@ ${LIBS}


all: ${BINDIR}/${BINPREF}faroo.build
all: ${BINDIR}/${BINPREF}faroo.demo
all: ${BINDIR}/${BINPREF}stringdiff.demo
	BUILT $^
$(info ${OBJ})
$(info $(DEP))
-include $(DEP)
