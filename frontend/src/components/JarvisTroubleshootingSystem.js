import React, { useState, useEffect } from 'react';
import { ChevronRight, AlertCircle, CheckCircle, Calculator, FileText, Search, TestTube, Settings, BarChart3, Wrench, Target, Lightbulb, Play, ArrowRight, Info } from 'lucide-react';

const JarvisTroubleshootingSystem = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [sessionData, setSessionData] = useState({});
  const [isActive, setIsActive] = useState(false);
  const [stepResults, setStepResults] = useState({});
  const [userInputs, setUserInputs] = useState({});

  // Step definitions matching your PDF document
  const steps = [
    { id: 'facility_data', name: 'Facility Data', icon: Calculator, description: 'Calculate all facility parameters (19 formulas)' },
    { id: 'problem_selection', name: 'Problem Selection', icon: Search, description: 'Select and verify the problem type' },
    { id: 'training_verification', name: 'Training & Verification', icon: CheckCircle, description: 'TSS analysis and discharge limit comparison' },
    { id: 'source_identification', name: 'Source Identification', icon: Target, description: 'Calculate L1-L9 contributions and percentages' },
    { id: 'inspection', name: 'Inspection', icon: Search, description: 'Only for L3, L6 - observation scoring' },
    { id: 'testing', name: 'Testing', icon: TestTube, description: 'Execute required tests based on inspection' },
    { id: 'evaluation', name: 'Evaluation', icon: BarChart3, description: 'Combine observations and test results' },
    { id: 'troubleshooting', name: 'Troubleshooting', icon: Wrench, description: 'Implement solutions in priority order' },
    { id: 'outcomes', name: 'Outcomes', icon: FileText, description: 'Monitor solution effectiveness' },
    { id: 'recommendations', name: 'Recommendations', icon: Lightbulb, description: 'Final recommendations if problem persists' }
  ];

  // Welcome screen when user asks for troubleshooting help
  const WelcomeScreen = () => (
    <div className="text-center p-8 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg">
      <div className="mb-6">
        <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <Wrench className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">JARVIS Troubleshooting System</h1>
        <p className="text-lg text-gray-600">AI-powered wastewater treatment diagnostic and solution system</p>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 className="text-xl font-semibold mb-4">10-Step Diagnostic Process</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {steps.map((step, index) => {
            const IconComponent = step.icon;
            return (
              <div key={index} className="text-center p-3 bg-gray-50 rounded-lg">
                <IconComponent className="w-6 h-6 mx-auto mb-2 text-blue-600" />
                <p className="text-xs font-medium">{step.name}</p>
              </div>
            );
          })}
        </div>
      </div>
      
      <button
        onClick={() => setIsActive(true)}
        className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center gap-2 mx-auto"
      >
        <Play className="w-5 h-5" />
        Start Troubleshooting Process
      </button>
    </div>
  );

  // Step 1: Facility Data
  const FacilityDataStep = () => {
    const [inputs, setInputs] = useState({
      influent_flow: '',
      diverted_flow: '',
      bod_concentration: '',
      total_vol_aeration_basin: '',
      mlss_concentration: '',
      total_vol_secondary_clarifier: '',
      ras_flow: '',
      ras_concentration: '',
      was_flow_gpm: '',
      mins_operation_per_hr: '60',
      surface_area_aeration_basin: '',
      surface_area_secondary_clarifier: '',
      total_weir_length: '',
      do_concentration: ''
    });

    const [calculations, setCalculations] = useState({});

    const calculateAll = () => {
      const results = {};
      
      // Formula 1: Total influent BOD (lbs/day)
      const influentFlow = parseFloat(inputs.influent_flow) || 0;
      const divertedFlow = parseFloat(inputs.diverted_flow) || 0;
      const bodConc = parseFloat(inputs.bod_concentration) || 0;
      results.total_influent_bod = (influentFlow - divertedFlow) * bodConc * 8.34;

      // Formula 2: Total MLVSS (lbs)
      const totalVolAB = parseFloat(inputs.total_vol_aeration_basin) || 0;
      const mlssConc = parseFloat(inputs.mlss_concentration) || 0;
      results.total_mlvss = totalVolAB * mlssConc * 8.34 * 0.75; // Assuming M/M ratio 0.75

      // Formula 3: F/M Ratio
      if (results.total_mlvss > 0) {
        results.fm_ratio = results.total_influent_bod / results.total_mlvss;
      }

      // Formula 5: Solids Inventory - Aeration Basin
      results.solids_inventory_ab = totalVolAB * mlssConc * 8.34;

      // Formula 11: HLR (Hydraulic Loading Rate)
      const rasFlow = parseFloat(inputs.ras_flow) || 0;
      const surfaceAreaAB = parseFloat(inputs.surface_area_aeration_basin) || 0;
      if (surfaceAreaAB > 0) {
        results.hlr = ((influentFlow - divertedFlow + rasFlow) * 1000000) / surfaceAreaAB;
      }

      // Formula 12: OLR (Organic Loading Rate)
      if (surfaceAreaAB > 0) {
        results.olr = results.total_influent_bod / surfaceAreaAB;
      }

      setCalculations(results);
      setStepResults({...stepResults, facility_data: { inputs, calculations: results }});
    };

    return (
      <div className="p-6">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Calculator className="w-6 h-6 text-blue-600" />
          Step 1: Facility Data - Calculate Parameters
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-1">Influent Flow (MGD)</label>
            <input
              type="number"
              value={inputs.influent_flow}
              onChange={(e) => setInputs({...inputs, influent_flow: e.target.value})}
              className="w-full p-2 border rounded-lg"
              placeholder="e.g., 2.5"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Diverted Flow (MGD)</label>
            <input
              type="number"
              value={inputs.diverted_flow}
              onChange={(e) => setInputs({...inputs, diverted_flow: e.target.value})}
              className="w-full p-2 border rounded-lg"
              placeholder="e.g., 0.2"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">BOD Concentration (mg/L)</label>
            <input
              type="number"
              value={inputs.bod_concentration}
              onChange={(e) => setInputs({...inputs, bod_concentration: e.target.value})}
              className="w-full p-2 border rounded-lg"
              placeholder="e.g., 250"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">MLSS Concentration (mg/L)</label>
            <input
              type="number"
              value={inputs.mlss_concentration}
              onChange={(e) => setInputs({...inputs, mlss_concentration: e.target.value})}
              className="w-full p-2 border rounded-lg"
              placeholder="e.g., 3500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">Total Volume Aeration Basin (million gal)</label>
            <input
              type="number"
              value={inputs.total_vol_aeration_basin}
              onChange={(e) => setInputs({...inputs, total_vol_aeration_basin: e.target.value})}
              className="w-full p-2 border rounded-lg"
              placeholder="e.g., 1.5"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-1">RAS Flow (MGD)</label>
            <input
              type="number"
              value={inputs.ras_flow}
              onChange={(e) => setInputs({...inputs, ras_flow: e.target.value})}
              className="w-full p-2 border rounded-lg"
              placeholder="e.g., 1.0"
            />
          </div>
        </div>

        <button
          onClick={calculateAll}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 mb-4"
        >
          Calculate All Parameters
        </button>

        {Object.keys(calculations).length > 0 && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-3">Calculated Results:</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="font-medium">Total Influent BOD:</span> {calculations.total_influent_bod?.toFixed(2)} lbs/day
              </div>
              <div>
                <span className="font-medium">Total MLVSS:</span> {calculations.total_mlvss?.toFixed(2)} lbs
              </div>
              <div>
                <span className="font-medium">F/M Ratio:</span> {calculations.fm_ratio?.toFixed(3)}
              </div>
              <div>
                <span className="font-medium">Solids Inventory AB:</span> {calculations.solids_inventory_ab?.toFixed(2)} lbs
              </div>
              {calculations.hlr && (
                <div>
                  <span className="font-medium">HLR:</span> {calculations.hlr?.toFixed(2)} gal/day/sq.ft
                </div>
              )}
              {calculations.olr && (
                <div>
                  <span className="font-medium">OLR:</span> {calculations.olr?.toFixed(3)} lbs/day/sq.ft
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    );
  };

  // Step 2: Problem Selection
  const ProblemSelectionStep = () => {
    const [selectedProblem, setSelectedProblem] = useState('');
    
    const problems = [
      'TSS (Total Suspended Solids)',
      'BOD (Biochemical Oxygen Demand)',
      'Ammonia',
      'Phosphorus',
      'pH Issues',
      'Dissolved Oxygen Problems',
      'Sludge Settlement Issues'
    ];

    return (
      <div className="p-6">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Search className="w-6 h-6 text-blue-600" />
          Step 2: Problem Selection
        </h3>
        
        <p className="text-gray-600 mb-4">Select the primary problem you're experiencing:</p>
        
        <div className="space-y-3 mb-6">
          {problems.map((problem) => (
            <label key={problem} className="flex items-center p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
              <input
                type="radio"
                name="problem"
                value={problem}
                checked={selectedProblem === problem}
                onChange={(e) => setSelectedProblem(e.target.value)}
                className="mr-3"
              />
              <span className="font-medium">{problem}</span>
            </label>
          ))}
        </div>

        {selectedProblem === 'TSS (Total Suspended Solids)' && (
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-blue-800">
              <strong>TSS Problem Selected:</strong> You will be directed to TSS-specific Training & Verification procedures.
            </p>
          </div>
        )}
      </div>
    );
  };

  // Step 3: Training & Verification
  const TrainingVerificationStep = () => {
    const [tssData, setTssData] = useState({
      weeklyValues: Array(7).fill(''),
      monthlyValues: Array(30).fill(''),
      weeklyLimit: '30',
      monthlyLimit: '30'
    });
    const [analysis, setAnalysis] = useState(null);

    const analyzeTSS = () => {
      const weeklyValues = tssData.weeklyValues.map(v => parseFloat(v) || 0).filter(v => v > 0);
      const monthlyValues = tssData.monthlyValues.map(v => parseFloat(v) || 0).filter(v => v > 0);
      
      const weeklyAvg = weeklyValues.length > 0 ? weeklyValues.reduce((a, b) => a + b, 0) / weeklyValues.length : 0;
      const monthlyAvg = monthlyValues.length > 0 ? monthlyValues.reduce((a, b) => a + b, 0) / monthlyValues.length : 0;
      
      const weeklyLimit = parseFloat(tssData.weeklyLimit);
      const monthlyLimit = parseFloat(tssData.monthlyLimit);
      
      let decision = 'PROBLEM_RESOLVED';
      let message = 'TSS is within discharge limits';
      let nextAction = 'end';
      
      if (weeklyAvg > weeklyLimit) {
        decision = 'PROBLEM_CONFIRMED';
        message = 'TSS exceeds Weekly Discharge Limit. Problem confirmed';
        nextAction = 'source_identification';
      } else if (monthlyAvg > monthlyLimit) {
        decision = 'PROBLEM_CONFIRMED';
        message = 'TSS exceeds Monthly Discharge Limit. Problem confirmed';
        nextAction = 'source_identification';
      }
      
      setAnalysis({
        weeklyAvg,
        monthlyAvg,
        weeklyLimit,
        monthlyLimit,
        decision,
        message,
        nextAction
      });
      
      setStepResults({...stepResults, training_verification: {
        weeklyAvg, monthlyAvg, decision, nextAction
      }});
    };

    return (
      <div className="p-6">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <CheckCircle className="w-6 h-6 text-blue-600" />
          Step 3: Training & Verification - TSS Analysis
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h4 className="font-semibold mb-3">Weekly TSS Values (mg/L)</h4>
            <div className="grid grid-cols-2 gap-2">
              {tssData.weeklyValues.map((value, index) => (
                <input
                  key={index}
                  type="number"
                  value={value}
                  onChange={(e) => {
                    const newValues = [...tssData.weeklyValues];
                    newValues[index] = e.target.value;
                    setTssData({...tssData, weeklyValues: newValues});
                  }}
                  placeholder={`Day ${index + 1}`}
                  className="p-2 border rounded text-sm"
                />
              ))}
            </div>
            
            <div className="mt-3">
              <label className="block text-sm font-medium mb-1">Weekly Discharge Limit (mg/L)</label>
              <input
                type="number"
                value={tssData.weeklyLimit}
                onChange={(e) => setTssData({...tssData, weeklyLimit: e.target.value})}
                className="w-full p-2 border rounded-lg"
              />
            </div>
          </div>
          
          <div>
            <h4 className="font-semibold mb-3">Sample Monthly TSS Values (mg/L)</h4>
            <div className="grid grid-cols-3 gap-2 max-h-32 overflow-y-auto">
              {tssData.monthlyValues.slice(0, 15).map((value, index) => (
                <input
                  key={index}
                  type="number"
                  value={value}
                  onChange={(e) => {
                    const newValues = [...tssData.monthlyValues];
                    newValues[index] = e.target.value;
                    setTssData({...tssData, monthlyValues: newValues});
                  }}
                  placeholder={`${index + 1}`}
                  className="p-1 border rounded text-xs"
                />
              ))}
            </div>
            
            <div className="mt-3">
              <label className="block text-sm font-medium mb-1">Monthly Discharge Limit (mg/L)</label>
              <input
                type="number"
                value={tssData.monthlyLimit}
                onChange={(e) => setTssData({...tssData, monthlyLimit: e.target.value})}
                className="w-full p-2 border rounded-lg"
              />
            </div>
          </div>
        </div>

        <button
          onClick={analyzeTSS}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 mb-4"
        >
          Analyze TSS Data
        </button>

        {analysis && (
          <div className={`p-4 rounded-lg ${analysis.decision === 'PROBLEM_CONFIRMED' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'} border`}>
            <div className="flex items-center gap-2 mb-3">
              {analysis.decision === 'PROBLEM_CONFIRMED' ? 
                <AlertCircle className="w-5 h-5 text-red-600" /> : 
                <CheckCircle className="w-5 h-5 text-green-600" />
              }
              <span className="font-semibold">{analysis.message}</span>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Weekly Average:</span> {analysis.weeklyAvg.toFixed(1)} mg/L
                <br />
                <span className="font-medium">Weekly Limit:</span> {analysis.weeklyLimit} mg/L
              </div>
              <div>
                <span className="font-medium">Monthly Average:</span> {analysis.monthlyAvg.toFixed(1)} mg/L
                <br />
                <span className="font-medium">Monthly Limit:</span> {analysis.monthlyLimit} mg/L
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  // Step 4: Source Identification
  const SourceIdentificationStep = () => {
    const [monitoringData, setMonitoringData] = useState({
      sec_effluent_stream: { flow: '', tss: '' },
      sec_clarifier_weirs: { flow: '', tss: '' },
      diverted_side_stream: { flow: '', tss: '' },
      primary_clarifier_weirs: { flow: '', tss: '' },
      aeration_basin_supernatant: { flow: '', tss: '' },
      splitter_box_supernatant: { flow: '', tss: '' },
      filtrate_sludge_handling: { flow: '', tss: '' },
      return_activated_sludge: { flow: '', tss: '' },
      waste_activated_sludge: { flow: '', tss: '' },
      raw_influent: { flow: '', tss: '' }
    });

    const [contributions, setContributions] = useState({});
    const [locationCode, setLocationCode] = useState('');

    const calculateContributions = () => {
      const results = {};
      
      // Extract values
      const flow1 = parseFloat(monitoringData.sec_effluent_stream.flow) || 0;
      const flow2 = parseFloat(monitoringData.sec_clarifier_weirs.flow) || 0;
      const flow3 = parseFloat(monitoringData.diverted_side_stream.flow) || 0;
      const flow4 = parseFloat(monitoringData.primary_clarifier_weirs.flow) || 0;
      
      const tss1 = parseFloat(monitoringData.sec_effluent_stream.tss) || 0;
      const tss2 = parseFloat(monitoringData.sec_clarifier_weirs.tss) || 0;
      const tss3 = parseFloat(monitoringData.diverted_side_stream.tss) || 0;
      const tss4 = parseFloat(monitoringData.primary_clarifier_weirs.tss) || 0;
      const tss5 = parseFloat(monitoringData.aeration_basin_supernatant.tss) || 0;

      // L1: Spill in Sec Eff Stream
      if ((flow2 * tss2) + (flow3 * tss3) < (flow1 * tss1)) {
        const l1_qty = ((flow1 * tss1) - (flow2 * tss2) - (flow3 * tss3)) * 8.34e-6;
        results['L1'] = {
          quantity: l1_qty,
          description: 'Spill in Sec Eff Stream',
          percentage: 0
        };
      }

      // L2: Diverted side-stream issues
      if (tss4 < tss3) {
        const l2_qty = (flow3 * (tss3 - tss4)) * 8.34e-6;
        results['L2'] = {
          quantity: l2_qty,
          description: 'Diverted side-stream (sec bypass) - Spill',
          percentage: 0
        };
      }

      // L3: Aeration Basin underperformance
      const l3_qty = (flow4 - flow3) * (tss5 - (0.2 * tss4)) * 8.34e-6;
      if (l3_qty > 0) {
        results['L3'] = {
          quantity: l3_qty,
          description: 'Aeration Basin underperformance',
          percentage: 0
        };
      }

      // Calculate percentages
      const totalContribution = Object.values(results).reduce((sum, item) => sum + item.quantity, 0);
      Object.keys(results).forEach(key => {
        results[key].percentage = totalContribution > 0 ? (results[key].quantity / totalContribution) * 100 : 0;
      });

      // Generate location code (sorted by percentage)
      const sortedLocations = Object.entries(results)
        .sort(([,a], [,b]) => b.percentage - a.percentage)
        .map(([key]) => key);
      
      setContributions(results);
      setLocationCode(sortedLocations.join('|'));
      setStepResults({...stepResults, source_identification: {
        contributions: results,
        locationCode: sortedLocations.join('|')
      }});
    };

    return (
      <div className="p-6">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Target className="w-6 h-6 text-blue-600" />
          Step 4: Source Identification - Calculate TSS Contributions
        </h3>
        
        <div className="mb-6">
          <h4 className="font-semibold mb-3">Monitoring Data (Table 1)</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(monitoringData).map(([location, data]) => (
              <div key={location} className="p-3 border rounded-lg">
                <h5 className="font-medium text-sm mb-2">
                  {location.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </h5>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    value={data.flow}
                    onChange={(e) => setMonitoringData({
                      ...monitoringData,
                      [location]: { ...data, flow: e.target.value }
                    })}
                    placeholder="Flow (gal/day)"
                    className="p-1 border rounded text-xs"
                  />
                  <input
                    type="number"
                    value={data.tss}
                    onChange={(e) => setMonitoringData({
                      ...monitoringData,
                      [location]: { ...data, tss: e.target.value }
                    })}
                    placeholder="TSS (mg/L)"
                    className="p-1 border rounded text-xs"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={calculateContributions}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 mb-4"
        >
          Calculate TSS Contributions
        </button>

        {Object.keys(contributions).length > 0 && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-3">TSS Contributions (Table 2)</h4>
            <div className="space-y-2">
              {Object.entries(contributions)
                .sort(([,a], [,b]) => b.percentage - a.percentage)
                .map(([location, data]) => (
                  <div key={location} className="flex justify-between items-center p-2 bg-white rounded">
                    <span className="font-medium">{location}: {data.description}</span>
                    <span className="text-blue-600 font-semibold">{data.percentage.toFixed(1)}%</span>
                  </div>
                ))}
            </div>
            
            {locationCode && (
              <div className="mt-4 p-3 bg-blue-50 rounded">
                <span className="font-medium">Generated Location Code: </span>
                <span className="font-mono text-blue-600">{locationCode}</span>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  // Step 5: Inspection (Only for L3, L6)
  const InspectionStep = () => {
    const requiresInspection = stepResults.source_identification?.locationCode?.includes('L3') || 
                              stepResults.source_identification?.locationCode?.includes('L6');

    if (!requiresInspection) {
      return (
        <div className="p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Search className="w-6 h-6 text-blue-600" />
            Step 5: Inspection
          </h3>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-green-800">
              <CheckCircle className="w-5 h-5 inline mr-2" />
              Inspection step skipped - only required for L3 and L6 locations.
            </p>
          </div>
        </div>
      );
    }

    const [observations, setObservations] = useState({
      L6: { selected: [] },
      L3: { selected: [] }
    });

    const observationOptions = {
      L6: ['DN', 'SP', 'HL', 'OG'],
      L3: ['DN', 'SP', 'HL', 'OG']
    };

    return (
      <div className="p-6">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Search className="w-6 h-6 text-blue-600" />
          Step 5: Inspection - L3, L6 Observations
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {['L6', 'L3'].map(location => (
            <div key={location} className="border rounded-lg p-4">
              <h4 className="font-semibold mb-3">Observations at {location}:</h4>
              <div className="space-y-2">
                {observationOptions[location].map(option => (
                  <label key={option} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={observations[location].selected.includes(option)}
                      onChange={(e) => {
                        const current = observations[location].selected;
                        const updated = e.target.checked 
                          ? [...current, option]
                          : current.filter(item => item !== option);
                        setObservations({
                          ...observations,
                          [location]: { selected: updated }
                        });
                      }}
                      className="mr-2"
                    />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold mb-2">Cumulative Observation Scores:</h4>
          <div className="text-sm">
            {['DN', 'SP', 'HL', 'OG'].map(cause => {
              const l6Count = observations.L6.selected.includes(cause) ? 1 : 0;
              const l3Count = observations.L3.selected.includes(cause) ? 1 : 0;
              const total = l6Count + l3Count;
              return (
                <div key={cause} className="flex justify-between py-1">
                  <span>{cause}:</span>
                  <span className="font-mono">{total}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  // Navigation
  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      // Check if we should skip steps based on results
      const currentStepData = stepResults[steps[currentStep].id];
      
      if (steps[currentStep].id === 'training_verification' && 
          currentStepData?.decision === 'PROBLEM_RESOLVED') {
        // Skip to end
        setCurrentStep(steps.length - 1);
        return;
      }
      
      if (steps[currentStep].id === 'source_identification' && 
          !currentStepData?.locationCode?.includes('L3') && 
          !currentStepData?.locationCode?.includes('L6')) {
        // Skip inspection and testing, go to troubleshooting
        setCurrentStep(7); // Troubleshooting
        return;
      }
      
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderCurrentStep = () => {
    if (!isActive) return <WelcomeScreen />;
    
    switch (steps[currentStep].id) {
      case 'facility_data': return <FacilityDataStep />;
      case 'problem_selection': return <ProblemSelectionStep />;
      case 'training_verification': return <TrainingVerificationStep />;
      case 'source_identification': return <SourceIdentificationStep />;
      case 'inspection': return <InspectionStep />;
      default:
        return (
          <div className="p-6 text-center">
            <h3 className="text-xl font-semibold mb-4">
              Step {currentStep + 1}: {steps[currentStep].name}
            </h3>
            <p className="text-gray-600 mb-4">This step is under development.</p>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-blue-800">
                This step would implement: {steps[currentStep].description}
              </p>
            </div>
          </div>
        );
    }
  };

  if (!isActive) {
    return <WelcomeScreen />;
  }

  return (
    <div className="max-w-6xl mx-auto p-4">
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">JARVIS Troubleshooting Pipeline</h2>
          <span className="text-sm text-gray-600">
            Step {currentStep + 1} of {steps.length}
          </span>
        </div>
        
        <div className="flex items-center space-x-2 mb-4">
          {steps.map((step, index) => {
            const IconComponent = step.icon;
            const isActive = index === currentStep;
            const isCompleted = index < currentStep || stepResults[step.id];
            
            return (
              <div key={index} className="flex items-center">
                <div className={`
                  flex items-center justify-center w-10 h-10 rounded-full
                  ${isActive ? 'bg-blue-600 text-white' : 
                    isCompleted ? 'bg-green-600 text-white' : 
                    'bg-gray-200 text-gray-600'}
                `}>
                  <IconComponent className="w-5 h-5" />
                </div>
                {index < steps.length - 1 && (
                  <div className={`w-8 h-1 ${isCompleted ? 'bg-green-600' : 'bg-gray-200'}`} />
                )}
              </div>
            );
          })}
        </div>
        
        <div className="bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          />
        </div>
      </div>

      {/* Current Step Content */}
      <div className="bg-white rounded-lg shadow-sm border">
        {renderCurrentStep()}
        
        {/* Navigation */}
        <div className="flex justify-between items-center p-6 border-t bg-gray-50">
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className={`px-4 py-2 rounded-lg ${
              currentStep === 0 
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed' 
                : 'bg-gray-600 text-white hover:bg-gray-700'
            }`}
          >
            Previous Step
          </button>
          
          <button
            onClick={nextStep}
            disabled={currentStep === steps.length - 1}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
              currentStep === steps.length - 1
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            Next Step
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
      
      {/* Session Data Debug (hidden in production) */}
      {Object.keys(stepResults).length > 0 && (
        <div className="mt-6 bg-gray-50 p-4 rounded-lg">
          <details>
            <summary className="cursor-pointer font-medium">Session Data (Debug)</summary>
            <pre className="mt-2 text-xs overflow-auto">
              {JSON.stringify(stepResults, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
};

export default JarvisTroubleshootingSystem;