# integrate_jarvis_fixed.py
"""
FIXED Integration for your exact setup
- Uses your jarvis_simple_db (not jarvis_comprehensive_db)
- Uses your FixedMultiSourceJarvisProcessor
- Integrates with your advanced_jarvis_features.py
"""

import sys
import os
sys.path.append('./src')

# Import your existing working components
from multi_folder_processor import FixedEnhancedJarvisChatbot
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

# Import your advanced features
from advanced_jarvis_features import (
    JarvisFormulaCalculator, JarvisQueryDetector, JarvisLogicGates,
    JarvisPipeline, JarvisDecisionTrees, AdvancedJarvisChatbot
)

class CompleteJarvisSystem:
    """
    Complete JARVIS system using YOUR existing components
    """
    
    def __init__(self):
        self.rag_chatbot = None
        self.advanced_chatbot = None
        self.system_ready = False
        
    def setup_system(self):
        """Setup using your exact working components"""
        
        print("🚀 Setting up Complete JARVIS System...")
        print("📁 Using your existing jarvis_simple_db database")
        
        # Step 1: Initialize your working RAG chatbot
        print("📚 Loading your FixedMultiSourceJarvisProcessor...")
        self.rag_chatbot = FixedEnhancedJarvisChatbot("./data/JARVIS_Knowledge_Base")
        
        # Step 2: Connect to YOUR actual working database
        print("🔗 Connecting to jarvis_simple_db...")
        embeddings = OllamaEmbeddings(model="llama2:13b-chat")
        
        # FIXED: Use YOUR actual database
        if os.path.exists("./jarvis_simple_db"):
            self.rag_chatbot.vector_store = Chroma(
                persist_directory="./jarvis_simple_db",  # YOUR actual DB
                embedding_function=embeddings
            )
            print("✅ Connected to jarvis_simple_db successfully!")
        else:
            print("❌ jarvis_simple_db not found!")
            print("💡 Make sure you've run your document processing first")
            return False
        
        # Step 3: Add your advanced features
        print("🔧 Adding your advanced JARVIS features...")
        self.advanced_chatbot = AdvancedJarvisChatbot(self.rag_chatbot)
        
        self.system_ready = True
        print("✅ Complete JARVIS system ready!")
        
        return True
    
    def query(self, query_text, session_id="default", input_data=None):
        """Main query interface"""
        
        if not self.system_ready:
            return {"error": "System not initialized. Call setup_system() first."}
        
        try:
            return self.advanced_chatbot.process_advanced_query(
                query_text, 
                session_id=session_id, 
                input_data=input_data
            )
        except Exception as e:
            return {"error": str(e), "query": query_text}
    
    def get_system_info(self):
        """Get system status"""
        
        if not self.system_ready:
            return {"status": "not_ready"}
        
        try:
            # Check database connection
            db_data = self.rag_chatbot.vector_store.get()
            docs_count = len(db_data['ids']) if db_data else 0
        except:
            docs_count = "unknown"
        
        return {
            "status": "ready",
            "database": "jarvis_simple_db",
            "documents": docs_count,
            "rag_system": "FixedEnhancedJarvisChatbot", 
            "advanced_features": "Full JARVIS capabilities enabled"
        }

# def test_your_system():
#     """Test the integrated system with your actual setup"""
    
#     print("🧪 TESTING YOUR INTEGRATED JARVIS SYSTEM")
#     print("=" * 50)
    
#     # Initialize
#     jarvis = CompleteJarvisSystem()
    
#     # Setup
#     if not jarvis.setup_system():
#         print("❌ Setup failed! Check your database and files.")
#         return False
    
#     # Check system info
#     info = jarvis.get_system_info()
#     print(f"📊 Status: {info['status']}")
#     print(f"📁 Database: {info['database']}")
#     print(f"📚 Documents: {info['documents']}")
    
#     # Test different query types
#     test_queries = [
#         {
#             'query': 'Calculate F/M ratio with influent flow 2.5 MGD, BOD 250 mg/L, MLSS 3500 mg/L',
#             'type': 'Calculation Test'
#         },
#         {
#             'query': 'What is F/M ratio and why is it important in wastewater treatment?',
#             'type': 'RAG Information Test'
#         },
#         {
#             'query': 'My TSS is 45 mg/L and discharge limit is 30 mg/L, help me diagnose',
#             'type': 'Diagnostic Test'
#         }
#     ]
    
#     print("\n🔍 Testing Query Capabilities:")
#     for test in test_queries:
#         print(f"\n--- {test['type']} ---")
#         print(f"Query: {test['query']}")
        
#         result = jarvis.query(test['query'])
        
#         if 'error' in result:
#             print(f"❌ Error: {result['error']}")
#         elif 'result' in result and 'formula_name' in result:
#             # Calculation result
#             print(f"✅ Formula: {result['formula_name']}")
#             print(f"📊 Result: {result['result']} {result.get('units', '')}")
#         elif 'answer' in result:
#             # RAG result
#             print(f"✅ RAG Answer: {result['answer'][:150]}...")
#             if 'source_files' in result:
#                 print(f"📁 Sources: {', '.join(result['source_files'][:2])}")
#         else:
#             print(f"✅ Response: {str(result)[:150]}...")
    
#     print("\n🎉 Integration test complete!")
#     print("Your system is working with:")
#     print("- Your existing RAG database (jarvis_simple_db)")
#     print("- Your FixedMultiSourceJarvisProcessor")
#     print("- All advanced JARVIS features")
    
#     return True

# def interactive_mode():
#     """Interactive mode for your system"""
    
#     print("\n🎮 INTERACTIVE JARVIS MODE")
#     print("Try your queries! Type 'quit' to exit.")
    
#     jarvis = CompleteJarvisSystem()
#     if not jarvis.setup_system():
#         print("❌ Failed to setup system!")
#         return
    
#     print("\n✅ System ready! Try these examples:")
#     print("1. Calculate F/M ratio with BOD 250 mg/L, MLSS 3500 mg/L")
#     print("2. What is SRT in wastewater treatment?")
#     print("3. My TSS exceeds limits, help me")
    
#     while True:
#         query = input("\n🔍 Your query: ").strip()
        
#         if query.lower() == 'quit':
#             print("👋 Goodbye!")
#             break
        
#         if not query:
#             continue
        
#         result = jarvis.query(query)
        
#         # Display result
#         if 'error' in result:
#             print(f"❌ Error: {result['error']}")
#         elif 'result' in result and 'formula_name' in result:
#             print(f"\n🧮 Calculation Result:")
#             print(f"Formula: {result['formula_name']}")
#             print(f"Result: {result['result']} {result.get('units', '')}")
#             if 'interpretation' in result:
#                 print(f"Interpretation: {result['interpretation']}")
#         elif 'answer' in result:
#             print(f"\n📝 Information:")
#             print(result['answer'])
#             if 'source_files' in result:
#                 print(f"\n📁 Sources: {', '.join(result['source_files'][:3])}")
#         else:
#             print(f"\n📊 Result: {result}")

# if __name__ == "__main__":
#     print("🎯 JARVIS INTEGRATION - Fixed for Your Setup")
#     print("Choose mode:")
#     print("1. Test system")
#     print("2. Interactive mode")
    
#     choice = input("Select (1 or 2): ").strip()
    
#     if choice == '2':
#         interactive_mode()
#     else:
#         test_your_system()