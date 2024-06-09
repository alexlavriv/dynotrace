#!/usr/bin/env python

import lldb
import os

def disassemble_instructions(insts):
    for i in insts:
        print i

# Set the path to the executable to debug
exe = "/home/alex/dev/dynotrace/a.out"

# Create a new debugger instance
debugger = lldb.SBDebugger.Create()

# When we step or continue, don't return from the function until the process
# stops. Otherwise we would have to handle the process events ourselves which, while doable is
#a little tricky.  We do this by setting the async mode to false.
debugger.SetAsync (False)

# Create a target from a file and arch
print  for '%s'" % exe

target = debugger.CreateTarget ('')

print "after creating target"
if target:
    print "before setting the targget"
    # If the target is valid set a breakpoint at main
    main_bp = target.BreakpointCreateByName ("print", target.GetExecutable().GetFilename());
    print "set bp"
    print main_bp

    # Launch the process. Since we specified synchronous mode, we won't return
    # from this function until we hit the breakpoint at main
    #process = target.LaunchSimple (None, None, os.getcwd())
    error = lldb.SBError()
    process = target.AttachToProcessWithName(debugger.GetListener(), 'test', False, error)

    # Make sure the launch went ok
    if process:
        # Print some simple process info
        state = process.GetState ()
	print "procrss state"
        print process
	print "The state is"
	print state
        while state != lldb.eStateExited:
	    process.Continue();
	    print "cont p"
            # Get the first thread
            thread = process.GetThreadAtIndex (0)
            if thread:
                # Print some simple thread info
		print "thread info"
                print thread
                # Get the first frame
                frame = thread.GetFrameAtIndex (0)
                if frame:
                    # Print some simple frame info
		    print "frame info"
                    print frame
                    function = frame.GetFunction()
                    # See if we have debug info (a function)
                    if function:
                        # We do have a function, print some info for the function
                        print function
                        # Now get all instructions for this function and print them
                        insts = function.GetInstructions(target)
                        disassemble_instructions (insts)
                    else:
                        # See if we have a symbol in the symbol table for where we stopped
                        symbol = frame.GetSymbol();
                        if symbol:
                            # We do have a symbol, print some info for the symbol
                            print symbol
		
else:
	print "target is none"
