import func
import config
from util.ProcessorData import ReadData

items, true_label = ReadData(config.fileData)

print("Dataset path: ", config.fileData)
print("Parameter: mL = ", config.mL, ", mU = ", config.mU, ", m = ", config.m, ", alpha = ", config.alpha)
func.run_FCM(config.number_clusters, config.Epsilon, config.m, config.max_iter)
func.run_MC_FCM()
func.run_sSMC_FCM()

