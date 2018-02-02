import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("Demo")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('RecoLocalCalo.HGCalRecProducers.HGCalLocalRecoSequence_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')
from FastSimulation.Event.ParticleFilter_cfi import *
from RecoLocalCalo.HGCalRecProducers.HGCalRecHit_cfi import dEdX_weights as dEdX

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/A0955ECB-20AA-E711-93A5-0CC47A7FC72C.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/82904FC5-53AA-E711-9A5E-0CC47A7FC72C.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/CC43DBBF-70AA-E711-99DD-3417EBE7047A.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/B6658543-91AA-E711-B0FE-3417EBE700D2.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/60978A53-73AA-E711-BBA0-002590DE6C56.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/A413A55B-95AA-E711-8E6E-002590DE3AC0.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/DAFE287F-A4AA-E711-96BE-002590DE6C56.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/4499EF85-45AB-E711-98A0-3417EBE705CD.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/5C42D49B-B8A9-E711-853F-0025901D4446.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/0CAE2259-F7AC-E711-9C77-001E6779245C.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/185568E3-BCAA-E711-AEED-002590E7D7CE.root',
'/store/mc/PhaseIITDRFall17DR/SingleElectronPt35Eta1p6_2p8/GEN-SIM-RECO/noPUFEVT_93X_upgrade2023_realistic_v2-v1/150000/46C40D81-49B1-E711-95DC-E0071B73B6D0.root'),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)

process.ana = cms.EDAnalyzer('HGCalAnalysis',
                             detector = cms.string("all"),
                             rawRecHits = cms.bool(False),
                             readCaloParticles = cms.bool(False),
                             storeGenParticleOrigin = cms.bool(True),
                             storeGenParticleExtrapolation = cms.bool(True),
                             storePCAvariables = cms.bool(False),
                             storeElectrons = cms.bool(True),
                             storePFCandidates = cms.bool(False),
                             readGenParticles = cms.bool(True),
                             recomputePCA = cms.bool(False),
                             includeHaloPCA = cms.bool(True),
                             dEdXWeights = dEdX,
                             layerClusterPtThreshold = cms.double(-1),  # All LayerCluster belonging to a multicluster are saved; this Pt threshold applied to the others
#                             disabledLayers = cms.vint(3, 10, 17, 24, 34,46), # 24,11,11
                             disabledLayers = cms.vint(2,4,7,10,13,16,19,22,25,27,30,34,38,42,46,50),   #18, 9, 9                             
                             TestParticleFilter = ParticleFilterBlock.ParticleFilter
)

process.ana.TestParticleFilter.protonEMin = cms.double(100000)
process.ana.TestParticleFilter.etaMax = cms.double(3.1)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("hgcalNtuple.root")

                                   )

reRunClustering = False

if reRunClustering:
    #process.hgcalLayerClusters.minClusters = cms.uint32(0)
    #process.hgcalLayerClusters.realSpaceCone = cms.bool(True)
    #process.hgcalLayerClusters.multiclusterRadius = cms.double(2.)  # in cm if realSpaceCone is true
    #process.hgcalLayerClusters.dependSensor = cms.bool(True)
    #process.hgcalLayerClusters.ecut = cms.double(3.)  # multiple of sigma noise if dependSensor is true
    #process.hgcalLayerClusters.kappa = cms.double(9.)  # multiple of sigma noise if dependSensor is true
    #process.hgcalLayerClusters.deltac = cms.vdouble(2.,3.,5.) #specify delta c for each subdetector separately
    process.p = cms.Path(process.hgcalLayerClusters+process.ana)
else:
    process.p = cms.Path(process.ana)
