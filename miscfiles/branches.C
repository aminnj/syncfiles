#include <TString.h>
#include <TFile.h>

gErrorIgnoreLevel=kError;

void branches(TString input)
{
    TFile *_file0 = TFile::Open(input);
    for(int i = 0; i < Events->GetListOfAliases()->LastIndex(); i++) 
        std::cout << "branch: " << Events->GetListOfAliases()->At(i)->GetName() << std::endl;
}
