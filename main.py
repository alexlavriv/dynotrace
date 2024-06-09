import lldb
import os
import sys

def disassemble_instructions (insts):
    for i in insts:
        print i

# Set the path to the executable to debug
exe = "./a.out"
# Create a new debugger instance
debugger = lldb.SBDebugger.Create()

# When we step or continue, don't return from the function until the process
# stops. We do this by setting the async mode to false.
debugger.SetAsync (False)

# Create a target from a file and arch
print('Creating a target for %s' % exe)

#target = debugger.CreateTarget (exe)
target = debugger.CreateTarget('')
if target:
    # If the target is valid set a breakpoint at main
    main_bp = target.BreakpointCreateByName("print",target.GetExecutable().GetFilename());

    print main_bp
    error = lldb.SBError()
    process = target.AttachToProcessWithID(debugger.GetListener(), 18603, error)

    # Launch the process. Since we specified synchronous mode, we won't return
    # from this function until we hit the breakpoint at main
    #process = target.LaunchSimple (None, None, os.getcwd())
    
    #error = lldb.SBError()
    #target.Launch(debugger.GetListener(), None, None,
    #                        None, '/tmp/stdout.txt', None,
    #                        None, 0, False, error)
    print error
    # Make sure the launch went ok
    if process:
        # Print some simple process info
        state = process.GetState ()
        print process
        while state == lldb.eStateStopped:
            # Get the first thread
            thread = process.GetThreadAtIndex (0)
            if thread:
                # Print some simple thread info
                print thread
                # Get the first frame
                frame = thread.GetFrameAtIndex (0)
                if frame:
                    # Print some simple frame info
                    print frame
                    function = frame.GetFunction()
		    var_k = frame.FindVariable('k');
		    print 'k val is: ', var_k.value 
                    # See if we have debug info (a function)
                    if function:
                        # We do have a function, print some info for the function
                        print function
                        # Now get all instructions for this function and print them
                        insts = function.GetInstructions(target)
                        #disassemble_instructions (insts)
                    else:
                        # See if we have a symbol in the symbol table for where we stopped
                        symbol = frame.GetSymbol();
                        if symbol:
                            # We do have a symbol, print some info for the symbol
                            #print symbol
                            # Now get all instructions for this symbol and print them
                            insts = symbol.GetInstructions(target)
                            #disassemble_instructions (insts)

                    registerList = frame.GetRegisters()
                    print('Frame registers (size of register set = %d):' % registerList.GetSize())
                    #for value in registerList:
                        #print value
                        #print('%s (number of children = %d):' % (value.GetName(), value.GetNumChildren()))
                        #for child in value:
                            #print('Name: ', child.GetName(), ' Value: ', child.GetValue())

            print('Hit the breakpoint at main, enter to continue and wait for program to exit or Ctrl-D quit to terminate the program')
            #next = sys.stdin.readline()
            #if not next or next.rstrip('') == 'quit':
            #    print('Terminating the inferior process...')
            #    process.Kill()
            #else:
            #    # Now continue to the program exit
            process.Continue()
                # When we return from the above function we will hopefully be at the
                # program exit. Print out some process info
            print process
            if state == lldb.eStateExited:
            	print('Didnt hit the breakpoint at main, program has exited...')
        
          #print('Unexpected process state: %s, killing process...' % debugger.StateAsCString (state))
          #process.Kill()
