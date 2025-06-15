# fixed_multi_folder_processor.py
import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.vectorstores.utils import filter_complex_metadata
import json
from langchain.vectorstores import Chroma
class FixedMultiSourceJarvisProcessor:
    """
    Fixed version that handles ChromaDB metadata limitations
    """
    
    def __init__(self, base_folder_path: str):
        self.base_path = Path(base_folder_path)
        self.step_mapping = {
            1: "facility_data",
            2: "problem_selection", 
            3: "training_verification",
            4: "source_identification",
            5: "inspection",
            6: "testing",
            7: "evaluation",
            8: "troubleshooting",
            9: "outcomes",
            10: "recommendations"
        }
        
    def process_all_folders(self) -> List[Document]:
        """Process all 10 folders and return list of documents for RAG"""
        
        all_documents = []
        
        print("🔄 Processing JARVIS Knowledge Base...")
        
        # Process each step folder
        for step_num in range(1, 11):
            step_name = self.step_mapping[step_num]
            
            # Try different folder naming patterns
            possible_names = [
                f"Step_{step_num}_{step_name.replace('_', '_').title()}",
                f"Step_{step_num}_{step_name}",
                f"Step{step_num}_{step_name}",
                f"{step_num}_{step_name}",
                f"Step {step_num} {step_name.replace('_', ' ').title()}",
                f"Step{step_num}"
            ]
            
            folder_found = False
            for folder_name in possible_names:
                folder_path = self.base_path / folder_name
                if folder_path.exists():
                    print(f"📁 Processing {folder_name}...")
                    step_documents = self.process_step_folder(folder_path, step_num, step_name)
                    all_documents.extend(step_documents)
                    print(f"   ✅ Added {len(step_documents)} documents")
                    folder_found = True
                    break
            
            if not folder_found:
                print(f"   ⚠️  No folder found for step {step_num} ({step_name})")
        
        print(f"🎉 Total documents processed: {len(all_documents)}")
        return all_documents
    
    def process_step_folder(self, folder_path: Path, step_num: int, step_name: str) -> List[Document]:
        """Process all files in a single step folder"""
        
        documents = []
        
        # Get all files in the folder
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == '.xlsx':
                        docs = self.process_excel_file(file_path, step_num, step_name)
                    elif file_path.suffix.lower() == '.pdf':
                        docs = self.process_pdf_file(file_path, step_num, step_name)
                    elif file_path.suffix.lower() in ['.docx', '.doc']:
                        docs = self.process_word_file(file_path, step_num, step_name)
                    else:
                        continue  # Skip unsupported file types
                    
                    documents.extend(docs)
                    
                except Exception as e:
                    print(f"   ❌ Error processing {file_path.name}: {str(e)}")
        
        return documents
    
    def process_excel_file(self, file_path: Path, step_num: int, step_name: str) -> List[Document]:
        """Process Excel files - tables, formulas, data"""
        
        documents = []
        
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Convert to text content
                content = f"Sheet: {sheet_name}\n\n"
                content += df.to_string(index=False)
                
                # Extract any formulas or calculations
                formulas = self.extract_excel_formulas(df)
                
                # FIXED: Convert complex metadata to simple strings
                metadata = {
                    'source_file': file_path.name,
                    'sheet_name': sheet_name,
                    'step_number': step_num,
                    'step_name': step_name,
                    'file_type': 'excel',
                    'data_rows': df.shape[0] if not df.empty else 0,
                    'data_cols': df.shape[1] if not df.empty else 0,
                    'columns': ', '.join(list(df.columns)) if not df.empty else '',
                    'has_formulas': len(formulas) > 0,
                    'formula_count': len(formulas)
                }
                
                # Create main document
                doc = Document(page_content=content, metadata=metadata)
                documents.append(doc)
                
                # Create separate documents for each formula (not in metadata)
                for i, formula in enumerate(formulas):
                    formula_content = f"Formula from {file_path.name} (Sheet: {sheet_name}):\n\n"
                    formula_content += f"Formula: {formula['formula']}\n"
                    formula_content += f"Context: {formula['context']}\n"
                    formula_content += f"Type: {formula['type']}"
                    
                    formula_metadata = {
                        'source_file': file_path.name,
                        'sheet_name': sheet_name,
                        'step_number': step_num,
                        'step_name': step_name,
                        'file_type': 'formula',
                        'formula_index': i,
                        'formula_type': formula['type']
                    }
                    
                    formula_doc = Document(
                        page_content=formula_content,
                        metadata=formula_metadata
                    )
                    documents.append(formula_doc)
        
        except Exception as e:
            print(f"Error processing Excel file {file_path}: {e}")
        
        return documents
    
    def process_pdf_file(self, file_path: Path, step_num: int, step_name: str) -> List[Document]:
        """Process PDF files"""
        
        documents = []
        
        try:
            loader = PyPDFLoader(str(file_path))
            pdf_docs = loader.load()
            
            for i, doc in enumerate(pdf_docs):
                # Extract any formulas or calculations from the text
                formulas = self.extract_text_formulas(doc.page_content)
                
                # FIXED: Simple metadata only
                doc.metadata = {
                    'source_file': file_path.name,
                    'page_number': i + 1,
                    'step_number': step_num,
                    'step_name': step_name,
                    'file_type': 'pdf',
                    'has_formulas': len(formulas) > 0,
                    'formula_count': len(formulas)
                }
                
                documents.append(doc)
                
                # Create separate documents for formulas
                for j, formula in enumerate(formulas):
                    formula_content = f"Formula from {file_path.name} (Page {i+1}):\n\n"
                    formula_content += f"Formula: {formula['formula']}\n"
                    formula_content += f"Context: {formula['context']}\n"
                    formula_content += f"Type: {formula['type']}"
                    
                    formula_doc = Document(
                        page_content=formula_content,
                        metadata={
                            'source_file': file_path.name,
                            'page_number': i + 1,
                            'step_number': step_num,
                            'step_name': step_name,
                            'file_type': 'formula',
                            'formula_index': j,
                            'formula_type': formula['type']
                        }
                    )
                    documents.append(formula_doc)
        
        except Exception as e:
            print(f"Error processing PDF file {file_path}: {e}")
        
        return documents
    
    def process_word_file(self, file_path: Path, step_num: int, step_name: str) -> List[Document]:
        """Process Word documents"""
        
        documents = []
        
        try:
            loader = Docx2txtLoader(str(file_path))
            word_docs = loader.load()
            
            for doc in word_docs:
                # Extract any formulas or calculations from the text
                formulas = self.extract_text_formulas(doc.page_content)
                
                # FIXED: Simple metadata only
                doc.metadata = {
                    'source_file': file_path.name,
                    'step_number': step_num,
                    'step_name': step_name,
                    'file_type': 'word',
                    'has_formulas': len(formulas) > 0,
                    'formula_count': len(formulas)
                }
                
                documents.append(doc)
                
                # Create separate documents for formulas
                for j, formula in enumerate(formulas):
                    formula_content = f"Formula from {file_path.name}:\n\n"
                    formula_content += f"Formula: {formula['formula']}\n"
                    formula_content += f"Context: {formula['context']}\n"
                    formula_content += f"Type: {formula['type']}"
                    
                    formula_doc = Document(
                        page_content=formula_content,
                        metadata={
                            'source_file': file_path.name,
                            'step_number': step_num,
                            'step_name': step_name,
                            'file_type': 'formula',
                            'formula_index': j,
                            'formula_type': formula['type']
                        }
                    )
                    documents.append(formula_doc)
        
        except Exception as e:
            print(f"Error processing Word file {file_path}: {e}")
        
        return documents
    
    def extract_excel_formulas(self, df: pd.DataFrame) -> List[Dict[str, str]]:
        """Extract formulas and calculations from Excel data"""
        
        formulas = []
        
        # Look for columns that might contain formulas
        for col in df.columns:
            col_str = str(col).lower()
            if any(keyword in col_str for keyword in ['formula', 'calculation', 'equation', '=']):
                for idx, value in df[col].items():
                    if pd.notna(value) and '=' in str(value):
                        formulas.append({
                            'formula': str(value),
                            'context': f"Column: {col}, Row: {idx}",
                            'type': 'excel_formula'
                        })
        
        # Look for cells that might be calculations
        for col in df.select_dtypes(include=['object']).columns:
            for idx, value in df[col].items():
                if pd.notna(value):
                    value_str = str(value)
                    if any(op in value_str for op in [' = ', ' × ', ' ÷', ' + ', ' - ']):
                        formulas.append({
                            'formula': value_str,
                            'context': f"Column: {col}, Row: {idx}",
                            'type': 'calculation'
                        })
        
        return formulas
    
    def extract_text_formulas(self, text: str) -> List[Dict[str, str]]:
        """Extract formulas from text content"""
        
        import re
        formulas = []
        
        # Pattern for equations (something = something)
        equation_pattern = r'([A-Za-z][A-Za-z0-9\s]*)\s*=\s*([^.!?]*)'
        matches = re.findall(equation_pattern, text)
        
        for match in matches:
            left_side, right_side = match
            if len(right_side.strip()) > 0 and len(right_side.strip()) < 200:  # Reasonable length
                formulas.append({
                    'formula': f"{left_side.strip()} = {right_side.strip()}",
                    'context': 'Extracted from text',
                    'type': 'text_formula'
                })
        
        return formulas


# FIXED Enhanced Chatbot Class
class FixedEnhancedJarvisChatbot:
    """
    Fixed chatbot that handles ChromaDB metadata limitations
    """
    
    def __init__(self, folders_path: str):
        from langchain.llms import Ollama
        from langchain.vectorstores import Chroma
        from langchain.embeddings import OllamaEmbeddings
        
        # Initialize Ollama (your existing setup)
        self.llm = Ollama(model="llama2:13b-chat")
        self.embeddings = OllamaEmbeddings(model="llama2:13b-chat")
        
        # Process all your folders
        self.processor = FixedMultiSourceJarvisProcessor(folders_path)
        self.vector_store = None
        self.documents = []
        
    def setup_knowledge_base(self):
        """Setup knowledge base from all your folders"""
        
        print("🚀 Setting up JARVIS Knowledge Base...")
        
        # Process all folders
        self.documents = self.processor.process_all_folders()
        
        # FIXED: Handle different document types and filter metadata
        print("🔄 Cleaning and validating documents...")
        filtered_documents = []
        
        for i, doc in enumerate(self.documents):
            try:
                # Check if it's a tuple (some loaders return tuples)
                if isinstance(doc, tuple):
                    print(f"   ⚠️  Found tuple at index {i}, converting to Document...")
                    if len(doc) >= 2:
                        # Assume tuple is (content, metadata)
                        content = doc[0] if doc[0] else ""
                        metadata = doc[1] if isinstance(doc[1], dict) else {}
                    else:
                        content = str(doc[0]) if doc[0] else ""
                        metadata = {}
                    
                    # Create proper Document object
                    from langchain.schema import Document
                    doc = Document(page_content=content, metadata=metadata)
                
                # Ensure it's a Document object
                if not hasattr(doc, 'metadata') or not hasattr(doc, 'page_content'):
                    print(f"   ⚠️  Invalid document at index {i}, skipping...")
                    continue
                
                # Clean metadata manually (safer than filter_complex_metadata)
                clean_metadata = {}
                for key, value in doc.metadata.items():
                    if isinstance(value, (str, int, float, bool)) or value is None:
                        clean_metadata[key] = value
                    elif isinstance(value, list):
                        # Convert list to string
                        clean_metadata[key] = ', '.join(str(v) for v in value[:5])  # First 5 items
                    elif isinstance(value, dict):
                        # Convert dict to string
                        clean_metadata[key] = str(value)[:100]  # First 100 chars
                    else:
                        # Convert other types to string
                        clean_metadata[key] = str(value)[:100]
                
                # Create clean document
                clean_doc = Document(
                    page_content=doc.page_content,
                    metadata=clean_metadata
                )
                
                filtered_documents.append(clean_doc)
                
            except Exception as e:
                print(f"   ❌ Error processing document {i}: {str(e)}")
                continue
        
        print(f"✅ Cleaned {len(filtered_documents)} documents")
        
        # Create vector store with filtered documents
        print("🔄 Creating vector embeddings...")
        self.vector_store = Chroma.from_documents(
            documents=filtered_documents,
            embedding=self.embeddings,
            persist_directory="./jarvis_comprehensive_db"
        )
        
        print("✅ Knowledge base setup complete!")
        return len(filtered_documents)
    
    def query_step_specific(self, query: str, step_number: int = None) -> Dict[str, Any]:
        """Query specific to a step or general query"""
        
        # Build search filter
        search_filter = {}
        if step_number:
            search_filter["step_number"] = step_number
        
        # Search relevant documents
        if search_filter:
            relevant_docs = self.vector_store.similarity_search(
                query, k=5, filter=search_filter
            )
        else:
            relevant_docs = self.vector_store.similarity_search(query, k=8)
        
        # Group documents by type for better context
        docs_by_type = {}
        for doc in relevant_docs:
            file_type = doc.metadata.get('file_type', 'unknown')
            if file_type not in docs_by_type:
                docs_by_type[file_type] = []
            docs_by_type[file_type].append(doc)
        
        # Build comprehensive context
        context_parts = []
        for file_type, docs in docs_by_type.items():
            context_parts.append(f"\n--- {file_type.upper()} SOURCES ---")
            for doc in docs:
                source_info = f"File: {doc.metadata.get('source_file', 'Unknown')}"
                if 'step_name' in doc.metadata:
                    source_info += f" (Step: {doc.metadata['step_name']})"
                context_parts.append(f"{source_info}")
                context_parts.append(doc.page_content[:500] + "...")
        
        context = "\n".join(context_parts)
        
        # Generate response using LLM
        prompt = f"""
        Based on the JARVIS wastewater treatment system documentation:
        
        Query: {query}
        
        Relevant Information:
        {context}
        
        Please provide a comprehensive answer that:
        1. Directly answers the question
        2. References specific formulas or procedures when applicable
        3. Provides step-by-step guidance if needed
        4. Mentions any important warnings or considerations
        5. Suggests next steps if appropriate
        
        Answer:
        """
        
        response = self.llm.invoke(prompt)
        
        return {
            'answer': response,
            'sources_used': len(relevant_docs),
            'source_files': list(set([doc.metadata.get('source_file', 'Unknown') for doc in relevant_docs])),
            'steps_referenced': list(set([doc.metadata.get('step_name', 'Unknown') for doc in relevant_docs if 'step_name' in doc.metadata]))
        }


# FIXED Simple setup function
def setup_your_fixed_chatbot():
    """
    Fixed function to set up your chatbot with your folder structure
    """
    
    # Point this to your main folder containing the 10 step folders
    your_folders_path = "./data/JARVIS_Knowledge_Base"  # CHANGE THIS IF DIFFERENT
    
    # Create chatbot
    chatbot = FixedEnhancedJarvisChatbot(your_folders_path)
    
    # Setup knowledge base (this will take a few minutes)
    num_docs = chatbot.setup_knowledge_base()
    print(f"📚 Loaded {num_docs} documents into knowledge base")
    
    return chatbot

# Test the fixed system
if __name__ == "__main__":
    # Example usage
    chatbot = setup_your_fixed_chatbot()
    
    # Test queries
    test_queries = [
        "How do I calculate F/M ratio?",
        "What should I do if TSS exceeds discharge limits?",
        "Show me the troubleshooting procedure for high BOD",
        "What are the inspection requirements for step 5?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result = chatbot.query_step_specific(query)
        print(f"📝 Answer: {result['answer'][:200]}...")
        print(f"📁 Sources: {result['source_files']}")