#include "RooDataHist.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooAbsPdf.h"
#include "RooPlot.h"
#include "RooFitResult.h"
#include "TH1.h"
#include "TSystem.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TPaveText.h"

/// include pdfs
#include "RooCBExGaussShape.h"
#include "RooCMSShape.h"

#include <vector>
#include <string>
#ifdef __CINT__
#pragma link C++ class std::vector<std::string>+;
#endif

using namespace RooFit;
using namespace std;

class tnpFitter {
public:
  tnpFitter( TFile *file, std::string histname  );
  tnpFitter( TH1 *hist, std::string histname  );
  ~tnpFitter(void) {if( _work != 0 ) delete _work; }
  void setZLineShapes(TH1 *hZ );
  void setWorkspace(std::vector<std::string>, bool isaddGaus=false);
  void setOutputFile(TFile *fOut ) {_fOut = fOut;}
  void fits(bool mcTruth,bool isMC,std::string title = "", bool isaddGaus=false);
  void useMinos(bool minos = true) {_useMinos = minos;}
  void textParForCanvas(RooFitResult *reshist, TPad *p);

  void setFitRange(double xMin,double xMax) { _xFitMin = xMin; _xFitMax = xMax; }
private:
  RooWorkspace *_work;
  std::string _histname_base;
  TFile *_fOut;
  double _nTot;
  bool _useMinos;
  double _xFitMin,_xFitMax;
  int _nBins = 10000;
};

tnpFitter::tnpFitter(TFile *filein, std::string histname   ) : _useMinos(false) {
  RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);
  _histname_base = histname;  

  TH1 *hist = (TH1*) filein->Get(TString::Format("%s",histname.c_str()).Data());

  _nTot = hist->Integral();
  /// MC histos are done between 50-130 to do the convolution properly
  /// but when doing MC fit in 60-120, need to zero bins outside the range
  for( int ib = 0; ib <= hist->GetXaxis()->GetNbins()+1; ib++ )
   if(  hist->GetXaxis()->GetBinCenter(ib) <= 60 || hist->GetXaxis()->GetBinCenter(ib) >= 120 ) {
     hist->SetBinContent(ib,0);
   }
  
  _work = new RooWorkspace("w") ;
  _work->factory("x[50,130]");

  RooDataHist roohist("hist","hist",*_work->var("x"),hist);
  _work->import(roohist) ;
  _xFitMin = 60;
  _xFitMax = 120;
}

tnpFitter::tnpFitter(TH1 *hist, std::string histname  ) : _useMinos(false) {
  RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);
  _histname_base = histname;
  
  _nTot = hist->Integral();
  /// MC histos are done between 50-130 to do the convolution properly
  /// but when doing MC fit in 60-120, need to zero bins outside the range
  for( int ib = 0; ib <= hist->GetXaxis()->GetNbins()+1; ib++ )
    if(  hist->GetXaxis()->GetBinCenter(ib) <= 60 || hist->GetXaxis()->GetBinCenter(ib) >= 120 ) {
      hist->SetBinContent(ib,0);
    }
  
  _work = new RooWorkspace("w") ;
  _work->factory("x[50,130]");
  
  RooDataHist roohist("hist","hist",*_work->var("x"),hist);
  _work->import(roohist) ;
  _xFitMin = 60;
  _xFitMax = 120;
  
}


void tnpFitter::setZLineShapes(TH1 *hZ) {
  RooDataHist roohist("hGenZ","hGenZ",*_work->var("x"),hZ);
  _work->import(roohist) ;
}

void tnpFitter::setWorkspace(std::vector<std::string> workspace, bool isaddGaus) {
  for( unsigned icom = 0 ; icom < workspace.size(); ++icom ) {
    _work->factory(workspace[icom].c_str());
  }

  _work->var("x")->setBins(_nBins, "cache");
  _work->factory("HistPdf::sigPhys(x,hGen,3)");
  _work->factory("FCONV::sig(x, sigPhys , sigRes)");
  _work->factory(TString::Format("nSig[%f,0.5,%f]",_nTot*0.9,_nTot*1.5));
  _work->factory(TString::Format("nBkg[%f,0.5,%f]",_nTot*0.1,_nTot*1.5));
}

void tnpFitter::fits(bool mcTruth,bool isMC,string title, bool isaddGaus) {

  cout << " title : " << title << endl;

  
  RooAbsPdf *pdf = _work->pdf("pdf");
  RooFitResult* res;

  if( mcTruth ) {
    _work->var("nBkg")->setVal(0); _work->var("nBkg")->setConstant();
    if( _work->var("sos")   ) { _work->var("sos")->setVal(0);
      _work->var("sos")->setConstant(); }
    if( _work->var("acms")  ) _work->var("acms")->setConstant();
    if( _work->var("beta")  ) _work->var("beta")->setConstant();
    if( _work->var("gamma") ) _work->var("gamma")->setConstant();
  }

  /// FC: seems to be better to change the actual range than using a fitRange in the fit itself (???)
  /// FC: I don't know why but the integral is done over the full range in the fit not on the reduced range
  _work->var("x")->setRange(_xFitMin,_xFitMax);
  _work->var("x")->setRange("fitMassRange",_xFitMin,_xFitMax);
  if( isMC == 1 ) res = pdf->fitTo(*_work->data("hist"), Minimizer("Minuit2", "MIGRAD"), Minos(_useMinos), Strategy(2), SumW2Error(kTRUE),Save(),Range("fitMassRange"));
  else res = pdf->fitTo(*_work->data("hist"), Minimizer("Minuit2", "MIGRAD"), Minos(_useMinos), Strategy(2), SumW2Error(kFALSE),Save(),Range("fitMassRange"));

  RooPlot *phist = _work->var("x")->frame(60,120);
  phist->SetTitle("histogram");
  
  _work->data("hist") ->plotOn( phist );
  _work->pdf("pdf")->plotOn( phist, LineColor(kRed) );
  _work->pdf("pdf")->plotOn( phist, Components("bkg"),LineColor(kBlue),LineStyle(kDashed));
  _work->data("hist") ->plotOn( phist );

  TCanvas c("c","c",1100,450);
  c.Divide(3,1);
  TPad *padText = (TPad*)c.GetPad(1);
  textParForCanvas( res, padText );
  c.cd(2); phist->Draw();

  _fOut->cd();
  c.Write(TString::Format("%s_Canv",_histname_base.c_str()),TObject::kOverwrite);
  res->Write(TString::Format("%s_res",_histname_base.c_str()),TObject::kOverwrite);

  
}





/////// Stupid parameter dumper /////////
void tnpFitter::textParForCanvas(RooFitResult *res,TPad *p) {

  double eff = -1;
  double e_eff = 0;

  RooRealVar *nSig = _work->var("nSig");
  
  double n   = nSig->getVal();
  double e_n = nSig->getError();

  TPaveText *text1 = new TPaveText(0,0.8,1,1);
  text1->SetFillColor(0);
  text1->SetBorderSize(0);
  text1->SetTextAlign(12);

  //  text->SetTextSize(0.06);

//  text->AddText("* Passing parameters");
  TPaveText *text = new TPaveText(0,0,1,0.8);
  text->SetFillColor(0);
  text->SetBorderSize(0);
  text->SetTextAlign(12);
  text->AddText("    --- parmeters " );
  RooArgList listParFinal = res->floatParsFinal();
  for( int ip = 0; ip < listParFinal.getSize(); ip++ ) {
    TString vName = listParFinal[ip].GetName();
    text->AddText(TString::Format("   - %s \t= %1.3f #pm %1.3f",
				  vName.Data(),
				  _work->var(vName)->getVal(),
				  _work->var(vName)->getError() ) );
  }


  p->cd();
  text1->Draw();
  text->Draw();
}
