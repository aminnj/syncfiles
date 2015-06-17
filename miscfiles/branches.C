#include <TString.h>
#include <TFile.h>

void branches(TString input)
{
    TFile *file = new TFile(input);
    TTree *tree = (TTree*)file->Get("Events");
    for(int i = 0; i < tree->GetListOfAliases()->LastIndex(); i++) 
        std::cout << "branch: " << tree->GetListOfAliases()->At(i)->GetName() << std::endl;
}
