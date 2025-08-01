import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import openai
from openai import OpenAI
from config import Config

# Import advanced intelligence systems
from core.agent_intelligence import (
    AgentPersonality, 
    AgentLearningSystem, 
    VectorMemorySystem, 
    PredictiveAnalytics
)

class BaseAgent:
    """Enhanced base class for all organizational agents with advanced AI capabilities"""
    
    def __init__(self, role: str, department: str, name: str = None):
        self.id = str(uuid.uuid4())
        self.role = role
        self.department = department
        self.name = name or f"{role}_Agent"
        self.created_at = datetime.now().isoformat()
        
        # Enhanced memory and intelligence systems
        self.memory = []  # Keep simple memory for backward compatibility
        self.vector_memory = VectorMemorySystem()
        self.learning_system = AgentLearningSystem()
        self.personality = AgentPersonality()
        self.predictive_analytics = PredictiveAnalytics()
        
        # Performance tracking
        self.current_workload = 0
        self.max_workload = 10
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.collaboration_score = 0.8
        self.performance_history = []
        
        # Task management
        self.active_tasks = []
        self.task_queue = []
        
        # Communication capabilities
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None
        
        # Initialize personality based on role
        self._initialize_role_personality()
        
    def _initialize_role_personality(self):
        """Initialize personality traits based on agent role"""
        role_personalities = {
            "CEO": {
                "risk_tolerance": 0.7,
                "leadership_assertiveness": 0.9,
                "decision_speed": 0.8,
                "innovation_appetite": 0.8
            },
            "CFO": {
                "risk_tolerance": 0.3,
                "analytical_approach": 0.9,
                "decision_speed": 0.6,
                "innovation_appetite": 0.4
            },
            "CTO": {
                "innovation_appetite": 0.9,
                "analytical_approach": 0.8,
                "risk_tolerance": 0.6,
                "adaptability": 0.8
            },
            "CMO": {
                "innovation_appetite": 0.8,
                "collaboration_style": 0.8,
                "communication_directness": 0.7,
                "adaptability": 0.7
            },
            "HR": {
                "collaboration_style": 0.9,
                "communication_directness": 0.6,
                "leadership_assertiveness": 0.6,
                "adaptability": 0.8
            }
        }
        
        if self.role in role_personalities:
            for trait, value in role_personalities[self.role].items():
                setattr(self.personality, trait, value)
    
    def add_memory(self, memory_item: Dict[str, Any], importance: float = 0.5):
        """Enhanced memory addition with vector embeddings"""
        # Add to simple memory (backward compatibility)
        memory_entry = {
            "content": memory_item.get("content", ""),
            "type": memory_item.get("type", "general"),
            "timestamp": datetime.now().isoformat(),
            "metadata": memory_item.get("metadata", {})
        }
        self.memory.append(memory_entry)
        
        # Add to vector memory for semantic search
        self.vector_memory.add_memory_with_embedding(
            content=memory_entry["content"],
            metadata={
                "type": memory_entry["type"],
                "agent_role": self.role,
                "department": self.department,
                **memory_entry["metadata"]
            },
            importance=importance
        )
        
        # Keep memory size manageable
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def get_relevant_memories(self, context: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant memories using advanced vector search"""
        # Try vector search first
        vector_results = self.vector_memory.search_memories_by_similarity(
            query=context,
            limit=limit,
            min_similarity=0.3
        )
        
        if vector_results:
            return vector_results
        
        # Fallback to simple keyword search
        context_words = context.lower().split()
        relevant_memories = []
        
        for memory in reversed(self.memory):
            content_words = memory["content"].lower().split()
            if any(word in content_words for word in context_words):
                relevant_memories.append(memory)
                if len(relevant_memories) >= limit:
                    break
        
        return relevant_memories
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent - to be overridden by subclasses"""
        personality_context = self._get_personality_context()
        
        return f"""
        You are a {self.role} in a technology startup. 
        
        PERSONALITY PROFILE:
        {personality_context}
        
        Always consider your personality traits when making decisions and communicating.
        Adapt your responses based on your current mood and stress level.
        Learn from past experiences and adjust your approach accordingly.
        """
    
    def _get_personality_context(self) -> str:
        """Get current personality state as context"""
        return f"""
        Current Mood: {self.personality.current_mood} (intensity: {self.personality.mood_intensity:.2f})
        Risk Tolerance: {self.personality.risk_tolerance:.2f}
        Collaboration Style: {self.personality.collaboration_style:.2f}
        Decision Speed: {self.personality.decision_speed:.2f}
        Innovation Appetite: {self.personality.innovation_appetite:.2f}
        Stress Level: {self.personality.stress_level:.2f}
        Confidence Level: {self.personality.confidence_level:.2f}
        Workload Pressure: {self.personality.workload_pressure:.2f}
        """
    
    def communicate_with_llm(self, prompt: str, context: str = "", use_learning: bool = True) -> str:
        """Enhanced LLM communication with learning and personality"""
        if not self.client:
            return f"[Simulated response from {self.role}]: Based on the request, I would analyze the situation and provide strategic guidance."
        
        try:
            # Get learning recommendations
            learning_context = ""
            if use_learning:
                recommendation = self.learning_system.get_recommended_approach(context)
                if recommendation["confidence"] > 0.5:
                    learning_context = f"\nBased on past experience, recommended approach: {recommendation['recommendation']} (confidence: {recommendation['confidence']:.2f})"
            
            # Get relevant memories
            relevant_memories = self.get_relevant_memories(context)
            memory_context = ""
            if relevant_memories:
                memory_context = "\nRelevant past experiences:\n" + "\n".join([
                    f"- {mem['content'][:100]}..." for mem in relevant_memories[:3]
                ])
            
            # Construct full prompt with personality and learning context
            full_prompt = f"""
            {self.get_system_prompt()}
            
            {learning_context}
            {memory_context}
            
            Context: {context}
            
            Request: {prompt}
            
            Respond in character, considering your personality, mood, and past experiences.
            """
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": full_prompt}
                ],
                max_tokens=Config.MAX_TOKENS_PER_RESPONSE,
                temperature=Config.TEMPERATURE
            )
            
            response_text = response.choices[0].message.content
            
            # Record decision for learning (if this was a decision-making context)
            if any(keyword in prompt.lower() for keyword in ["decide", "recommend", "strategy", "plan"]):
                # Assume positive outcome for now - in real system, this would be tracked
                self.learning_system.record_decision(context, response_text, 0.7)
            
            return response_text
            
        except Exception as e:
            error_response = f"Error communicating with LLM: {str(e)}"
            self.add_memory({
                "content": f"Failed to get LLM response: {str(e)}",
                "type": "error",
                "metadata": {"context": context}
            })
            return error_response
    
    def assign_task(self, task: Dict[str, Any]) -> bool:
        """Enhanced task assignment with workload and personality consideration"""
        if self.current_workload >= self.max_workload:
            return False
        
        # Adjust task acceptance based on personality
        if task.get("risk_level", "medium") == "high" and self.personality.risk_tolerance < 0.4:
            if self.personality.stress_level > 0.7:
                return False  # Too stressed for high-risk tasks
        
        task["assigned_at"] = datetime.now().isoformat()
        task["status"] = "assigned"
        task["agent_id"] = self.id
        
        self.active_tasks.append(task)
        self.current_workload += task.get("complexity", 1)
        
        # Update personality based on workload
        workload_ratio = self.current_workload / self.max_workload
        self.personality.adjust_for_workload(workload_ratio)
        
        # Add task to memory
        self.add_memory({
            "content": f"Assigned task: {task.get('description', 'No description')}",
            "type": "task_assignment",
            "metadata": {"task_id": task.get("id"), "complexity": task.get("complexity", 1)}
        })
        
        return True
    
    def complete_task(self, task_id: str, success: bool = True, outcome_details: str = "") -> Dict[str, Any]:
        """Enhanced task completion with learning and personality updates"""
        completed_task = None
        
        for i, task in enumerate(self.active_tasks):
            if task.get("id") == task_id:
                completed_task = self.active_tasks.pop(i)
                break
        
        if not completed_task:
            return {"status": "error", "message": "Task not found"}
        
        # Update workload
        self.current_workload -= completed_task.get("complexity", 1)
        self.current_workload = max(0, self.current_workload)
        
        # Update performance tracking
        if success:
            self.completed_tasks += 1
        else:
            self.failed_tasks += 1
        
        # Update personality based on outcome
        impact_magnitude = completed_task.get("importance", 0.5)
        self.personality.update_from_outcome(success, impact_magnitude)
        
        # Record performance metrics
        self.predictive_analytics.add_data_point("task_success_rate", 
                                                1.0 if success else 0.0)
        
        # Add completion to memory
        completion_memory = {
            "content": f"Completed task: {completed_task.get('description', 'No description')}. Success: {success}. {outcome_details}",
            "type": "task_completion",
            "metadata": {
                "task_id": task_id,
                "success": success,
                "outcome_details": outcome_details,
                "complexity": completed_task.get("complexity", 1)
            }
        }
        self.add_memory(completion_memory, importance=0.7 if success else 0.8)
        
        # Update performance history
        performance_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "success": success,
            "complexity": completed_task.get("complexity", 1),
            "outcome_details": outcome_details
        }
        self.performance_history.append(performance_entry)
        
        # Keep performance history manageable
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-50:]
        
        return {
            "status": "completed",
            "task": completed_task,
            "success": success,
            "personality_update": {
                "mood": self.personality.current_mood,
                "confidence": self.personality.confidence_level,
                "stress": self.personality.stress_level
            }
        }
    
    def make_decision(self, decision_context: str, options: List[str]) -> Dict[str, Any]:
        """Enhanced decision making with personality and learning influence"""
        # Get learning recommendation
        learning_rec = self.learning_system.get_recommended_approach(decision_context)
        
        # Adjust decision process based on personality
        decision_prompt = f"""
        Given the following decision context and options, choose the best option and explain your reasoning.
        
        Consider your personality traits:
        - Risk tolerance: {self.personality.risk_tolerance:.2f}
        - Decision speed: {self.personality.decision_speed:.2f}
        - Innovation appetite: {self.personality.innovation_appetite:.2f}
        - Current mood: {self.personality.current_mood}
        
        Learning recommendation: {learning_rec.get('recommendation', 'balanced')} (confidence: {learning_rec.get('confidence', 0):.2f})
        
        Context: {decision_context}
        Options: {', '.join(options)}
        
        Provide your choice and reasoning.
        """
        
        response = self.communicate_with_llm(decision_prompt, decision_context)
        
        # Extract decision (simple heuristic - in production would use more sophisticated parsing)
        chosen_option = options[0]  # Default
        for option in options:
            if option.lower() in response.lower():
                chosen_option = option
                break
        
        decision_result = {
            "chosen_option": chosen_option,
            "reasoning": response,
            "confidence": min(1.0, self.personality.confidence_level + learning_rec.get('confidence', 0) * 0.3),
            "influenced_by_learning": learning_rec.get('confidence', 0) > 0.5,
            "personality_factors": {
                "risk_tolerance": self.personality.risk_tolerance,
                "decision_speed": self.personality.decision_speed,
                "mood": self.personality.current_mood
            }
        }
        
        # Record decision for learning
        self.learning_system.record_decision(decision_context, chosen_option, 0.7)  # Assume positive outcome initially
        
        return decision_result
    
    def collaborate(self, other_agent_role: str, collaboration_context: str) -> Dict[str, Any]:
        """Enhanced collaboration with learning from past interactions"""
        # Check collaboration history
        collaboration_history = self.learning_system.collaboration_history.get(other_agent_role, [])
        
        if collaboration_history:
            avg_quality = sum(h["quality"] for h in collaboration_history[-5:]) / len(collaboration_history[-5:])
            collaboration_context += f"\n\nPast collaboration quality with {other_agent_role}: {avg_quality:.2f}"
        
        collaboration_prompt = f"""
        Collaborate with the {other_agent_role} on the following matter.
        
        Your collaboration style: {self.personality.collaboration_style:.2f}
        Your communication directness: {self.personality.communication_directness:.2f}
        
        Context: {collaboration_context}
        
        Provide your collaborative input and suggestions.
        """
        
        response = self.communicate_with_llm(collaboration_prompt, collaboration_context)
        
        # Record collaboration
        collaboration_quality = 0.7  # Default - would be calculated based on actual outcomes
        self.learning_system.learn_from_collaboration(other_agent_role, collaboration_quality, "successful")
        
        return {
            "collaboration_input": response,
            "collaboration_quality": collaboration_quality,
            "personality_influence": {
                "collaboration_style": self.personality.collaboration_style,
                "communication_directness": self.personality.communication_directness
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Enhanced status including personality and learning insights"""
        # Get performance predictions
        performance_prediction = self.predictive_analytics.predict_trend("task_success_rate")
        
        return {
            "id": self.id,
            "role": self.role,
            "department": self.department,
            "name": self.name,
            "current_workload": self.current_workload,
            "max_workload": self.max_workload,
            "workload_percentage": (self.current_workload / self.max_workload) * 100,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": self.completed_tasks / max(1, self.completed_tasks + self.failed_tasks),
            "collaboration_score": self.collaboration_score,
            
            # Enhanced status with personality and learning
            "personality": {
                "mood": self.personality.current_mood,
                "mood_intensity": self.personality.mood_intensity,
                "confidence_level": self.personality.confidence_level,
                "stress_level": self.personality.stress_level,
                "risk_tolerance": self.personality.risk_tolerance,
                "innovation_appetite": self.personality.innovation_appetite
            },
            
            "learning_insights": {
                "decision_patterns_learned": len(self.learning_system.decision_patterns),
                "collaboration_partners": len(self.learning_system.collaboration_history),
                "recent_successes": self.personality.recent_successes,
                "recent_failures": self.personality.recent_failures
            },
            
            "predictions": {
                "performance_trend": performance_prediction.get("trend", "unknown"),
                "predicted_success_rate": performance_prediction.get("next_value", 0.7),
                "prediction_confidence": performance_prediction.get("confidence", 0.5)
            },
            
            "memory_stats": {
                "total_memories": len(self.memory),
                "vector_memories": len(self.vector_memory.memories),
                "memory_index_size": len(self.vector_memory.memory_index)
            }
        }
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a specific task - to be overridden by subclasses"""
        context = f"Processing {task.get('type', 'general')} task: {task.get('description', '')}"
        
        response = self.communicate_with_llm(
            f"Handle this task: {task.get('description', 'No description provided')}",
            context
        )
        
        return {
            "status": "completed",
            "response": response,
            "processed_by": self.role
        } 