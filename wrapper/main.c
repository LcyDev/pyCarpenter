#include <windows.h>
#include <shellapi.h>

#define LIB "\\libraries\\Wood.exe\""

int main(void) {
    SetConsoleTitleA("Loading Wood Rewritten...");

    // Construct the path to executable
    TCHAR path[MAX_PATH];

    GetModuleFileNameA(NULL, path, MAX_PATH) // Get current working dir
    PathRemoveFileSpecA(path); // Remove Launcher.exe from path
    PathAppend(path, LIB); // Append the library path

    // Use ShellExecuteEx for more control and visibility
    SHELLEXECUTEINFO sei = { sizeof(sei) };
    sei.lpVerb = "open";
    sei.lpFile = path;
    sei.nShow = SW_SHOWNORMAL;  // Show the launched window
    
	// Check for errors
    if (!ShellExecuteEx(&sei)) {
        // Handle error
        MessageBox(NULL, "Failed to launch Wood.exe", "Error", MB_ICONERROR);
        return 1;
    } 

    return 0;
}