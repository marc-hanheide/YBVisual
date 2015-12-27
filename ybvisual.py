#!/usr/bin/env python

# ---------------------------
# Defines the main executable file
# ---------------------------


#!/usr/bin/env python
from lib.tmux import *

if __name__ == "__main__":  
    print "hello world"
    manager = TMUXManager()
    manager.Load("lib/tsession.yaml")

