
import numpy as np

class Hist1D(object):
    
    def __init__(self, obj=None, **kwargs):
        tstr = str(type(obj))

        self._counts = None
        self._edges = None
        self._errors = None
        if "ROOT." in tstr:
            self.init_root(obj,**kwargs)
        elif "ndarray" in tstr:
            self.init_numpy(obj,**kwargs)

    def init_numpy(self, obj, **kwargs):
        if "errors" in kwargs:
            self._errors = kwargs["errors"]
            del kwargs["errors"]

        self._counts, self._edges = np.histogram(obj,**kwargs)

        # poisson defaults if not specified
        if self._errors is None:
            self._errors = np.sqrt(self._counts)

    def init_root(self, obj, **kwargs):
        low_edges = np.array([1.0*obj.GetBinLowEdge(ibin) for ibin in range(obj.GetNbinsX()+1)])
        bin_widths = np.array([1.0*obj.GetBinWidth(ibin) for ibin in range(obj.GetNbinsX()+1)])
        self._counts = np.array([1.0*obj.GetBinContent(ibin) for ibin in range(1,obj.GetNbinsX()+1)])
        self._errors = np.array([1.0*obj.GetBinError(ibin) for ibin in range(1,obj.GetNbinsX()+1)])
        self._edges = low_edges + bin_widths

    def get_errors(self):
        return self._errors

    def get_counts(self):
        return self._counts

    def get_edges(self):
        return self._edges

    def get_bin_centers(self):
        return 0.5*(self._edges[1:]+self._edges[:-1])

    def get_integral(self):
        return np.sum(self._counts)

    def _check_consistency(self, other):
        if len(self._edges) != len(other._edges):
            raise Exception("These histograms cannot be combined due to different binning")

    def __add__(self, other):
        self._check_consistency(other)
        hnew = Hist1D()
        hnew._counts = self._counts + other._counts
        hnew._errors = (self._errors**2. + other._errors**2.)**0.5
        hnew._edges = self._edges
        return hnew

    def __sub__(self, other):
        self._check_consistency(other)
        hnew = Hist1D()
        hnew._counts = self._counts - other._counts
        hnew._errors = (self._errors**2. + other._errors**2.)**0.5
        hnew._edges = self._edges
        return hnew

    def __div__(self, other):
        self._check_consistency(other)
        hnew = Hist1D()
        hnew._counts = self._counts / other._counts
        hnew._errors = (
                (self._errors/other._counts)**2.0 +
                (other._errors*self._counts/(other._counts)**2.0)**2.0
                )**0.5
        hnew._edges = self._edges
        return hnew

    def __repr__(self):
        use_ascii = False
        if use_ascii: sep = "+-"
        else: sep = u"\u00B1".encode("utf-8")
        # trick: want to use numpy's smart formatting (truncating,...) of arrays
        # so we convert value,error into a complex number and format that 1D array :)
        formatter = {"complex_kind": lambda x:"%.2f {} %.2f".format(sep)%(np.real(x),np.imag(x))}
        a2s = np.array2string(self._counts+self._errors*1j,formatter=formatter, suppress_small=True, separator="   ")
        return "<Hist1D:\n{}\n>".format(a2s)

if __name__ == "__main__":
    np.random.seed(42)

    # make a root histogram with 10k gaussians, and convert it into a Hist1D object
    nbins = 20
    N = 10000
    import ROOT as r
    hroot = r.TH1F("h1","h1",nbins,-3,3)
    hroot.FillRandom("gaus",N)
    h1 = Hist1D(hroot)

    # make a Hist1D object out of a numpy array of 10k gaussians, with same binning
    h2 = Hist1D(np.random.normal(0,1,N),bins=np.linspace(-3,3,nbins+1))

    print "Nice repr... h1/h2:"
    print h1/h2

