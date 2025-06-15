# src/jarvis_pipeline_handler.py
"""
Enhanced pipeline handler that connects React frontend with your pipeline steps
"""

from complete_jarvis_advanced_features import JarvisPipeline
from typing import Dict, Any

class EnhancedJarvisPipeline(JarvisPipeline):
    """
    Extended pipeline with frontend-friendly methods
    """
    
    def __init__(self, llm, vector_store, calculator, logic_gates):
        super().__init__(llm, vector_store, calculator, logic_gates)
        self.frontend_sessions = {}
    
    def start_frontend_session(self, session_id: str) -> Dict[str, Any]:
        """Start a new frontend troubleshooting session"""
        self.frontend_sessions[session_id] = {
            'current_step': 0,
            'step_data': {},
            'step_results': {},
            'created_at': None
        }
        
        return {
            'session_id': session_id,
            'current_step': 0,
            'status': 'started',
            'next_step': 'facility_data'
        }
    
    def execute_frontend_step(self, session_id: str, step_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute step with frontend session management"""
        
        if session_id not in self.frontend_sessions:
            self.start_frontend_session(session_id)
        
        session = self.frontend_sessions[session_id]
        
        # Execute the step using your existing pipeline
        result = self.execute_step(step_name, input_data)
        
        # Update session
        session['step_data'][step_name] = input_data
        session['step_results'][step_name] = result
        
        # Add frontend-specific info
        result['session_id'] = session_id
        result['session_data'] = session
        
        return result
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current session status"""
        if session_id not in self.frontend_sessions:
            return {'error': 'Session not found'}
        
        return self.frontend_sessions[session_id]