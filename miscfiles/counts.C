#include <TString.h>

void counts(TString input, TString treeName="Events")
{
    gErrorIgnoreLevel=kError;
    TChain * ch = new TChain(treeName);
    if(input.Contains(".root")) {
        ch->Add(input);
    } else {
        ch->Add(input+"/*.root");
    }
    std::cout << "Events: " << ch->GetEntries() << std::endl;
}
