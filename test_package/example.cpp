#include <iostream>
#include <quazip/quazip.h>

int main() {
    QuaZip zip;
    std::cout << zip.isOpen();
    return 0;
}
