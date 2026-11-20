# mpi3mr makefile
EXTRA_CFLAGS := -DVALIDATION_SUPPORT_CODE
obj-m += mpi3mr.o
mpi3mr-y +=  mpi3mr_os.o     \
		mpi3mr_fw.o \
		mpi3mr_app.o \
		mpi3mr_debugfs.o \
		mpi3mr_transport.o 


bsg_setup_queue_has_reply_len := $(shell \
    printf '%s\n' \
    '#include <linux/bsg-lib.h>' \
    'void probe(struct device *dev, struct queue_limits *lim)' \
    '{' \
    '	bsg_setup_queue(dev, "probe", lim, NULL, NULL, 0, 0);' \
    '}' | \
    $(CC) $(KBUILD_CPPFLAGS) $(KBUILD_CFLAGS) \
    -x c -c -o /dev/null - >/dev/null 2>&1 && echo y)

ifeq ($(bsg_setup_queue_has_reply_len),y)
ccflags-y += -DMPI3MR_BSG_SETUP_QUEUE_HAS_REPLY_LEN
endif
