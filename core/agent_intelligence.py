import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import math

@dataclass
class AgentPersonality:
    """Dynamic personality system that evolves based on experiences"""
    
    # Core personality traits (0.0 to 1.0)
    risk_tolerance: float = 0.5
    collaboration_style: float = 0.7
    decision_speed: float = 0.6
    innovation_appetite: float = 0.8
    communication_directness: float = 0.6
    analytical_approach: float = 0.7
    adaptability: float = 0.5
    leadership_assertiveness: float = 0.6
    
    # Dynamic state
    stress_level: float = 0.3
    confidence_level: float = 0.7
    workload_pressure: float = 0.4
    team_satisfaction: float = 0.8
    
    # Mood states
    current_mood: str = "neutral"  # happy, stressed, confident, frustrated, motivated
    mood_intensity: float = 0.5
    
    # Experience tracking
    recent_successes: int = 0
    recent_failures: int = 0
    learning_rate: float = 0.1
    
    def update_from_outcome(self, success: bool, impact_magnitude: float = 1.0):
        """Update personality based on task outcomes"""
        if success:
            self.recent_successes += 1
            self.confidence_level = min(1.0, self.confidence_level + 0.05 * impact_magnitude)
            self.stress_level = max(0.0, self.stress_level - 0.03 * impact_magnitude)
            
            # Successful outcomes slightly increase risk tolerance
            if impact_magnitude > 0.7:
                self.risk_tolerance = min(1.0, self.risk_tolerance + 0.02)
                
        else:
            self.recent_failures += 1
            self.confidence_level = max(0.0, self.confidence_level - 0.08 * impact_magnitude)
            self.stress_level = min(1.0, self.stress_level + 0.05 * impact_magnitude)
            
            # Failures make agent more conservative
            self.risk_tolerance = max(0.0, self.risk_tolerance - 0.03 * impact_magnitude)
        
        # Update mood based on recent performance
        self._update_mood()
    
    def _update_mood(self):
        """Update current mood based on personality state"""
        success_ratio = self.recent_successes / max(1, self.recent_successes + self.recent_failures)
        
        if self.confidence_level > 0.8 and success_ratio > 0.7:
            self.current_mood = "confident"
            self.mood_intensity = min(1.0, self.confidence_level)
        elif self.stress_level > 0.7:
            self.current_mood = "stressed"
            self.mood_intensity = self.stress_level
        elif success_ratio > 0.6:
            self.current_mood = "motivated"
            self.mood_intensity = success_ratio
        elif self.confidence_level < 0.3:
            self.current_mood = "frustrated"
            self.mood_intensity = 1.0 - self.confidence_level
        else:
            self.current_mood = "neutral"
            self.mood_intensity = 0.5
    
    def adjust_for_workload(self, workload_ratio: float):
        """Adjust personality based on current workload"""
        self.workload_pressure = workload_ratio
        
        if workload_ratio > 0.8:
            self.stress_level = min(1.0, self.stress_level + 0.1)
            self.decision_speed = max(0.2, self.decision_speed - 0.1)  # More careful when overloaded
        elif workload_ratio < 0.3:
            self.stress_level = max(0.0, self.stress_level - 0.05)
            self.innovation_appetite = min(1.0, self.innovation_appetite + 0.05)  # More creative when not busy

class AgentLearningSystem:
    """Advanced learning system that allows agents to improve over time"""
    
    def __init__(self):
        self.decision_patterns = {}
        self.strategy_effectiveness = {}
        self.collaboration_history = {}
        self.adaptation_strategies = []
        self.learning_memories = []
        
    def record_decision(self, decision_context: str, decision: str, outcome_quality: float):
        """Record a decision and its outcome for learning"""
        if decision_context not in self.decision_patterns:
            self.decision_patterns[decision_context] = []
        
        self.decision_patterns[decision_context].append({
            "decision": decision,
            "outcome_quality": outcome_quality,
            "timestamp": datetime.now().isoformat(),
            "context_hash": hashlib.md5(decision_context.encode()).hexdigest()[:8]
        })
        
        # Keep only recent decisions for each context
        if len(self.decision_patterns[decision_context]) > 10:
            self.decision_patterns[decision_context] = self.decision_patterns[decision_context][-10:]
    
    def get_recommended_approach(self, context: str) -> Dict[str, Any]:
        """Get recommended approach based on historical success"""
        similar_contexts = self._find_similar_contexts(context)
        
        if not similar_contexts:
            return {"recommendation": "explore", "confidence": 0.3}
        
        # Analyze successful patterns
        successful_decisions = []
        for ctx_decisions in similar_contexts:
            for decision_record in ctx_decisions:
                if decision_record["outcome_quality"] > 0.7:
                    successful_decisions.append(decision_record)
        
        if successful_decisions:
            # Find most common successful approach
            approach_counts = {}
            for decision in successful_decisions:
                approach = self._extract_approach_pattern(decision["decision"])
                approach_counts[approach] = approach_counts.get(approach, 0) + 1
            
            best_approach = max(approach_counts.items(), key=lambda x: x[1])
            confidence = best_approach[1] / len(successful_decisions)
            
            return {
                "recommendation": best_approach[0],
                "confidence": confidence,
                "supporting_examples": len(successful_decisions)
            }
        
        return {"recommendation": "balanced", "confidence": 0.4}
    
    def _find_similar_contexts(self, context: str, similarity_threshold: float = 0.6) -> List:
        """Find historically similar decision contexts"""
        context_words = set(context.lower().split())
        similar_contexts = []
        
        for ctx, decisions in self.decision_patterns.items():
            ctx_words = set(ctx.lower().split())
            
            # Simple word overlap similarity
            if ctx_words and context_words:
                similarity = len(ctx_words.intersection(context_words)) / len(ctx_words.union(context_words))
                if similarity >= similarity_threshold:
                    similar_contexts.append(decisions)
        
        return similar_contexts
    
    def _extract_approach_pattern(self, decision: str) -> str:
        """Extract high-level approach pattern from decision text"""
        decision_lower = decision.lower()
        
        # Simple pattern recognition
        if any(word in decision_lower for word in ["aggressive", "fast", "immediate", "urgent"]):
            return "aggressive"
        elif any(word in decision_lower for word in ["conservative", "careful", "gradual", "safe"]):
            return "conservative"
        elif any(word in decision_lower for word in ["innovative", "creative", "new", "experimental"]):
            return "innovative"
        elif any(word in decision_lower for word in ["collaborate", "team", "consensus", "together"]):
            return "collaborative"
        else:
            return "balanced"
    
    def learn_from_collaboration(self, other_agent_role: str, interaction_quality: float, outcome: str):
        """Learn from collaborative interactions"""
        if other_agent_role not in self.collaboration_history:
            self.collaboration_history[other_agent_role] = []
        
        self.collaboration_history[other_agent_role].append({
            "quality": interaction_quality,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep recent history
        if len(self.collaboration_history[other_agent_role]) > 20:
            self.collaboration_history[other_agent_role] = self.collaboration_history[other_agent_role][-20:]

class VectorMemorySystem:
    """Advanced memory system using vector embeddings for semantic search"""
    
    def __init__(self):
        self.memories = []
        self.embeddings = []
        self.memory_index = {}
        self.importance_weights = []
        
    def add_memory_with_embedding(self, content: str, metadata: Dict[str, Any], 
                                importance: float = 0.5, embedding: Optional[List[float]] = None):
        """Add memory with vector embedding for semantic search"""
        memory_id = len(self.memories)
        
        memory_entry = {
            "id": memory_id,
            "content": content,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat(),
            "importance": importance,
            "access_count": 0,
            "last_accessed": datetime.now().isoformat()
        }
        
        self.memories.append(memory_entry)
        self.importance_weights.append(importance)
        
        # For now, use simple text-based embedding simulation
        # In production, you'd use OpenAI embeddings API
        if embedding:
            self.embeddings.append(embedding)
        else:
            self.embeddings.append(self._create_simple_embedding(content))
        
        # Update search index
        self._update_search_index(memory_id, content, metadata)
    
    def _create_simple_embedding(self, text: str, dimensions: int = 100) -> List[float]:
        """Create a simple embedding based on text characteristics"""
        # This is a simplified embedding - in production use OpenAI embeddings
        words = text.lower().split()
        
        # Simple character and word-based features
        features = [
            len(text) / 1000,  # Text length
            len(words) / 100,  # Word count
            len(set(words)) / len(words) if words else 0,  # Vocabulary diversity
            sum(1 for w in words if len(w) > 6) / len(words) if words else 0,  # Complex words ratio
        ]
        
        # Pad or truncate to desired dimensions
        while len(features) < dimensions:
            features.append(random.uniform(-0.1, 0.1))
        
        return features[:dimensions]
    
    def search_memories_by_similarity(self, query: str, limit: int = 5, 
                                    min_similarity: float = 0.3) -> List[Dict[str, Any]]:
        """Search memories using vector similarity"""
        if not self.embeddings:
            return []
        
        query_embedding = self._create_simple_embedding(query)
        similarities = []
        
        for i, memory_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, memory_embedding)
            
            # Weight by importance and recency
            recency_weight = self._calculate_recency_weight(self.memories[i]["timestamp"])
            importance_weight = self.importance_weights[i]
            
            weighted_similarity = similarity * (0.6 + 0.2 * importance_weight + 0.2 * recency_weight)
            
            if weighted_similarity >= min_similarity:
                similarities.append((i, weighted_similarity))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for mem_id, similarity in similarities[:limit]:
            memory = self.memories[mem_id].copy()
            memory["similarity_score"] = similarity
            
            # Update access tracking
            self.memories[mem_id]["access_count"] += 1
            self.memories[mem_id]["last_accessed"] = datetime.now().isoformat()
            
            results.append(memory)
        
        return results
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _calculate_recency_weight(self, timestamp_str: str) -> float:
        """Calculate recency weight (more recent = higher weight)"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            time_diff = datetime.now() - timestamp
            days_old = time_diff.total_seconds() / (24 * 3600)
            
            # Exponential decay: weight decreases over time
            return math.exp(-days_old / 30)  # Half-life of ~21 days
        except:
            return 0.5
    
    def _update_search_index(self, memory_id: int, content: str, metadata: Dict[str, Any]):
        """Update keyword-based search index"""
        words = content.lower().split()
        
        for word in words:
            if len(word) > 2:  # Skip very short words
                if word not in self.memory_index:
                    self.memory_index[word] = []
                self.memory_index[word].append(memory_id)
        
        # Index metadata values
        for key, value in metadata.items():
            if isinstance(value, str):
                index_key = f"{key}:{value.lower()}"
                if index_key not in self.memory_index:
                    self.memory_index[index_key] = []
                self.memory_index[index_key].append(memory_id)

class PredictiveAnalytics:
    """Predictive analytics for agent performance and business metrics"""
    
    def __init__(self):
        self.historical_data = {}
        self.trend_models = {}
        self.prediction_accuracy = {}
        
    def add_data_point(self, metric_name: str, value: float, timestamp: str = None):
        """Add a data point for predictive modeling"""
        if metric_name not in self.historical_data:
            self.historical_data[metric_name] = []
        
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        self.historical_data[metric_name].append({
            "value": value,
            "timestamp": timestamp
        })
        
        # Keep reasonable history size
        if len(self.historical_data[metric_name]) > 1000:
            self.historical_data[metric_name] = self.historical_data[metric_name][-1000:]
    
    def predict_trend(self, metric_name: str, periods_ahead: int = 5) -> Dict[str, Any]:
        """Predict future values using simple trend analysis"""
        if metric_name not in self.historical_data or len(self.historical_data[metric_name]) < 3:
            return {"prediction": None, "confidence": 0.0, "trend": "insufficient_data"}
        
        data_points = self.historical_data[metric_name][-20:]  # Use recent data
        values = [point["value"] for point in data_points]
        
        # Simple linear trend calculation
        n = len(values)
        x = list(range(n))
        
        # Calculate slope (trend)
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        # Predict future values
        predictions = []
        for i in range(1, periods_ahead + 1):
            predicted_value = intercept + slope * (n + i - 1)
            predictions.append(predicted_value)
        
        # Calculate prediction confidence based on recent trend stability
        recent_values = values[-5:] if len(values) >= 5 else values
        variance = np.var(recent_values) if len(recent_values) > 1 else 0
        confidence = max(0.1, min(0.9, 1.0 - (variance / (np.mean(recent_values) + 0.001))))
        
        # Determine trend direction
        if abs(slope) < 0.01:
            trend = "stable"
        elif slope > 0:
            trend = "increasing"
        else:
            trend = "decreasing"
        
        return {
            "predictions": predictions,
            "trend": trend,
            "slope": slope,
            "confidence": confidence,
            "next_value": predictions[0] if predictions else None
        }
    
    def detect_anomalies(self, metric_name: str, threshold_std: float = 2.0) -> List[Dict[str, Any]]:
        """Detect anomalous values in the data"""
        if metric_name not in self.historical_data or len(self.historical_data[metric_name]) < 10:
            return []
        
        data_points = self.historical_data[metric_name]
        values = [point["value"] for point in data_points]
        
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        anomalies = []
        for i, point in enumerate(data_points):
            z_score = abs(point["value"] - mean_value) / (std_value + 0.001)
            
            if z_score > threshold_std:
                anomalies.append({
                    "index": i,
                    "value": point["value"],
                    "timestamp": point["timestamp"],
                    "z_score": z_score,
                    "severity": "high" if z_score > 3.0 else "medium"
                })
        
        return anomalies[-10:]  # Return recent anomalies

import random

# Simple random module since numpy isn't available in simulation
def random_uniform(low, high):
    return random.uniform(low, high) 