// #include <iostream>
// #include <TString.h>
// #include <TFile.h>
// #include <TTree.h>
#include <TString.h>

void counts(TString foldername)
// void counts(int test)
{

    // std::cout << filename << std::endl;
    TChain * ch = new TChain("Events");
    ch->Add(foldername+"/*.root");
    std::cout << "Events: " << ch->GetEntries() << std::endl;

}
