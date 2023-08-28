// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include "stdio.h"
#include <iostream>
/*BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
*/

void main() {
    cout<<"Hello World"<<
    int a = fgets("Enter something: ");
    fprintf(a);
}

main();