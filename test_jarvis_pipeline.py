# test_jarvis_pipeline.py
from src.advanced_jarvis_features import JarvisFormulaCalculator, JarvisLogicGates

# Test 1: Formula Calculator
calculator = JarvisFormulaCalculator()

# Test F/M ratio calculation
inputs = {
    'influent_flow': 2.5,
    'diverted_flow': 0.2, 
    'bod_concentration': 250,
    'total_vol_aeration_basin': 1.5,
    'mlss_concentration': 3500
}

# Calculate BOD load (Formula 1)
bod_result = calculator.calculate(1, inputs)
print("BOD Load:", bod_result)

# Calculate F/M ratio (Formula 3) 
fm_result = calculator.calculate(3, {
    'total_bod': bod_result['result'],
    'total_mlvss': 43762.5  # From Formula 2
})
print("F/M Ratio:", fm_result)

# Test 2: Logic Gates TSS Analysis
logic = JarvisLogicGates()
tss_values = [35, 38, 42, 45, 40, 37, 39]
result = logic.evaluate_tss_dl_comparison(tss_values, 30, "weekly")
print("TSS Analysis:", result)