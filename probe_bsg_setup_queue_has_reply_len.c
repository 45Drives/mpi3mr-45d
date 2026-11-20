#include <linux/bsg-lib.h>

void probe(struct device *dev, struct queue_limits *limits)
{
    bsg_setup_queue(dev, "probe", limits, NULL, NULL, 0, 0);
}
