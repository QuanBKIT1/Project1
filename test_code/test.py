import func
import config

print("Dataset path: ", config.fileData)
print("Parameter: mL = ", config.mL, ", mU = ", config.mU, ", m = ", config.m, ", alpha = ", config.alpha)
# func.run_FCM()
# func.run_MC_FCM()
func.run_sSMC_FCM()

