#include <TString.h>

void counts(TString input)
{
    TChain * ch = new TChain("Events");
    if(input.Contains(".root")) {
        ch->Add(input);
    } else {
        ch->Add(input+"/*.root");
    }
    std::cout << "Events: " << ch->GetEntries() << std::endl;
}
