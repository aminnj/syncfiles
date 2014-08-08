// #include <iostream>
// #include <TString.h>
// #include <TFile.h>
// #include <TTree.h>
#include <TString.h>

void counts(TString filename)
// void counts(int test)
{

    std::cout << filename << std::endl;
    TFile * fh = new TFile(filename);
    std::cout << "Events: " << Events->GetEntries() << std::endl;

}
