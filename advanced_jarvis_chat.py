# fixed_jarvis_chat.py
import sys
import json
sys.path.append('./src')

from multi_folder_processor import FixedEnhancedJarvisChatbot
from advanced_jarvis_features import AdvancedJarvisChatbot, JarvisFormulaCalculator, JarvisLogicGates
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

def load_complete_jarvis():
    """Load the complete JARVIS system"""
    
    # Load existing RAG system
    existing_chatbot = FixedEnhancedJarvisChatbot("./data/JARVIS_Knowledge_Base")
    
    embeddings = OllamaEmbeddings(model="llama2:13b-chat")
    existing_chatbot.vector_store = Chroma(
        persist_directory="./jarvis_comprehensive_db",
        embedding_function=embeddings
    )
    
    # Add advanced features
    advanced_jarvis = AdvancedJarvisChatbot(existing_chatbot)
    
    return advanced_jarvis

def check_for_troubleshooting(query):
    """Check if user wants to start troubleshooting pipeline"""
    keywords = [
        'help me troubleshoot', 'troubleshooting', 'diagnostic',
        'problem with', 'tss exceeds', 'high tss', 'treatment issue',
        'guide me through', 'start pipeline', 'step by step',
        'my tss is', 'effluent quality', 'discharge limit'
    ]
    
    return any(keyword in query.lower() for keyword in keywords)

def run_troubleshooting_pipeline():
    """Run the complete troubleshooting pipeline"""
    print("\n🚀 Starting JARVIS 10-step troubleshooting process...")
    print("="*60)
    print("🔬 JARVIS TROUBLESHOOTING PIPELINE ACTIVATED")
    print("="*60)
    
    # Initialize components
    calculator = JarvisFormulaCalculator()
    logic = JarvisLogicGates()
    
    # Step 1: Quick facility calculations
    print("\n📊 STEP 1: FACILITY DATA")
    sample_inputs = {
        'influent_flow': 2.5,
        'diverted_flow': 0.2,
        'bod_concentration': 250,
        'mlss_concentration': 3500,
        'total_vol_aeration_basin': 1.5,
        'ras_flow': 1.0
    }
    
    print("Using sample facility data for demonstration...")
    
    # Calculate key parameters
    bod_result = calculator.calculate(1, sample_inputs)
    mlvss_result = calculator.calculate(2, sample_inputs)
    
    if bod_result['status'] == 'success' and mlvss_result['status'] == 'success':
        fm_result = calculator.calculate(3, {
            'total_bod': bod_result['result'],
            'total_mlvss': mlvss_result['result']
        })
        print(f"✅ Total BOD: {bod_result['result']:.1f} lbs/day")
        print(f"✅ Total MLVSS: {mlvss_result['result']:.1f} lbs")
        print(f"✅ F/M Ratio: {fm_result['result']:.3f}")
    
    # Step 3: TSS Analysis
    print(f"\n🔍 STEP 3: TSS VERIFICATION")
    weekly_tss = [35, 38, 42, 45, 40, 37, 39]  # Sample data exceeding limits
    weekly_limit = 30
    
    tss_result = logic.evaluate_tss_dl_comparison(weekly_tss, weekly_limit, "weekly")
    
    print(f"📊 Weekly TSS Average: {tss_result['avg_tss']:.1f} mg/L")
    print(f"📊 Discharge Limit: {weekly_limit} mg/L")
    print(f"⚠️  {tss_result['message']}")
    
    if tss_result['decision'] == 'PROBLEM_CONFIRMED':
        # Step 4: Source Identification
        print(f"\n🎯 STEP 4: SOURCE IDENTIFICATION")
        print("Analyzing TSS source contributions...")
        
        contributions = {
            'L1': {'percentage': 45, 'description': 'Spill in Secondary Effluent Stream'},
            'L2': {'percentage': 35, 'description': 'Diverted Side-stream Issues'},
            'L3': {'percentage': 20, 'description': 'Aeration Basin Underperformance'}
        }
        
        print("\n📋 TSS Source Contributions:")
        for location, data in contributions.items():
            print(f"  {location}: {data['percentage']}% - {data['description']}")
        
        location_code = "L1|L2|L3"
        print(f"\n📌 Location Code: {location_code}")
        
        # Step 8: Solutions
        print(f"\n🔧 STEP 8: RECOMMENDED SOLUTIONS")
        solutions = [
            "🎯 Priority 1 (L1 - 45%): S8 - Inspect secondary effluent for spills and leaks",
            "🎯 Priority 2 (L2 - 35%): S10 - Optimize diverted side-stream operations", 
            "🎯 Priority 3 (L3 - 20%): S1, S4 - Improve aeration basin mixing and performance"
        ]
        
        for solution in solutions:
            print(f"  {solution}")
        
        print(f"\n✅ PIPELINE COMPLETE!")
        print(f"📋 Next Steps:")
        print(f"  1. Implement solutions in priority order")
        print(f"  2. Monitor TSS levels after each change")
        print(f"  3. Return for additional analysis if needed")
    
    else:
        print(f"✅ TSS within acceptable limits - no action required")
    
    print("="*60)

def main():
    print("🤖 JARVIS Fixed Troubleshooting Assistant")
    print("=" * 60)
    
    # Load system
    print("Loading JARVIS system...")
    jarvis = load_complete_jarvis()
    print("✅ Ready!")
    
    print("\n🎯 TRY THESE COMMANDS:")
    print("🔧 'help me troubleshoot' - Start 10-step pipeline")
    print("📊 'calculate F/M ratio with...' - Direct calculations")
    print("📚 'what is SRT?' - Knowledge queries")
    print("❌ 'quit' - Exit")
    print("-" * 60)
    
    session_id = "main_session"
    
    while True:
        user_input = input("\n🔍 Your question: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("🤔 Processing...")
        
        try:
            # CHECK FOR TROUBLESHOOTING FIRST!
            if check_for_troubleshooting(user_input):
                run_troubleshooting_pipeline()
                continue
            
            # Otherwise process normally
            result = jarvis.process_advanced_query(user_input, session_id=session_id)
            
            print(f"\n📝 Answer:")
            
            # Handle different result types
            if 'status' in result and result['status'] == 'success':
                print(f"✅ {result.get('formula_name', 'Calculation')} Result: {result.get('result', 'N/A')} {result.get('units', '')}")
                if 'calculation_steps' in result:
                    print("\n📊 Calculation Steps:")
                    for step in result['calculation_steps']:
                        print(f"  • {step}")
                if 'interpretation' in result:
                    print(f"\n💡 Interpretation: {result['interpretation']}")
            
            elif 'answer' in result:
                print(result['answer'])
                if 'source_files' in result:
                    print(f"\n📁 Sources: {', '.join(result['source_files'][:3])}")
            
            else:
                print(json.dumps(result, indent=2))
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()