// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"

BOOL APIENTRY DllMain( HMODULE hModule,
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


extern "C" {
    __declspec(dllexport) const std::vector<int> HelloWorld() {
        std::vector<int> myVector;
        myVector.push_back(5);
        myVector.push_back(4);
        myVector.push_back(2);

        return (char) myVector;
    }
}

class Node {
public:
    int value;
    Node* left;
    Node* right;

    Node();
    ~Node();
    void addToTree(int value);
    void printInOrder();
};

Node::Node()
{
    printf("Node constructor @ %p\n", this);
    left = NULL;
    right = NULL;
    value = 10000;
}

Node::~Node() {
    printf("Destroying node at %p\n", this);
    if (left) {
        delete left;
    }
    if (right) {
        delete right;
    }
}

void Node::addToTree(int valueTaken) {
    if (valueTaken <= value) {
        if (left == NULL) {
            left = new Node();
            left->value = valueTaken;
        }
        else {
            left->addToTree(valueTaken);
        }
    }
    if (valueTaken > value) {
        if (right == NULL) {
            right = new Node();
            right->value = valueTaken;
        }
        else {
            right->addToTree(valueTaken);
        }
    }

}

void Node::printInOrder() {
    if (left) {
        left->printInOrder();
    }
    printf("%d\n", value);
    if (right) {
        right->printInOrder();
    }
}



int factorial(int a) {
    int res = 1;
    for (int i = 1;i < a+1;i++) {
        res = res * i;
    }
    return res;
}

void printer(int* p, Node* root) {
    for (int i = 0;i < 101; i++) {
        root->addToTree(p[i]);
    }
}

int* myFunc() {
    int* p;
    p = (int*)malloc(404);
    if (!p) {
        exit(1);
    }
    for (int i = 0;i < 101; i++) {
        p[i] = rand() % 100000;
    }
    return p;
}


int __cdecl main() {
    int* res;
    res = myFunc();

    Node* root;
    root = new Node();
    root->value = 10000;
    printer(res, root);
    root->printInOrder();
    printf("Hello from main\n");

    char* p;
    p = (char*) malloc(30);
    if (!p) {
        exit(1);
    }
    strcpy(p, "This is a string");
    p[4] = 'b';
    printf("%s\n", p);
    printf("%p\n", p);
    printf("Size of an int is %llu\n", sizeof(int));

    int fact = factorial(5);
    printf("The result is: %d\n", fact);
    free(p);
    free(res);
    delete root;

    return 0;
}

