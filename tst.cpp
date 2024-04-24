#include "compass/tk/tk.h"

int main(int argc, char *argv[]) {
    Tk_Main(argc, argv, Tcl_AppInit);
    return 0;
}

int Tcl_AppInit(Tcl_Interp *interp) {
    Tk_MainWindow(interp);
    
    // Create a simple button
    Tk_CreateButton(interp, Tk_MainWindow(interp), "Hello", NULL, 0);
    
    // Start the Tk event loop
    Tk_MainLoop();
    
    return TCL_OK;
}

