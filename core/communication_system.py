import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    """Types of organizational messages"""
    TASK_ASSIGNMENT = "task_assignment"
    COLLABORATION_REQUEST = "collaboration_request"
    DECISION_NOTIFICATION = "decision_notification"
    STATUS_UPDATE = "status_update"
    MEETING_REQUEST = "meeting_request"
    BUDGET_REQUEST = "budget_request"
    APPROVAL_REQUEST = "approval_request"
    GENERAL_COMMUNICATION = "general_communication"
    CRISIS_ALERT = "crisis_alert"

class Priority(Enum):
    """Message priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

@dataclass
class Message:
    """Represents a message in the organizational communication system"""
    id: str
    sender_id: str
    receiver_id: str
    message_type: MessageType
    subject: str
    content: str
    priority: Priority
    created_at: datetime
    read_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class OrganizationalMemory:
    """Centralized organizational memory and knowledge management"""
    
    def __init__(self):
        self.knowledge_base = {}
        self.decisions_archive = []
        self.project_history = []
        self.lessons_learned = []
        self.best_practices = []
        self.organizational_events = []
        self.performance_history = {}
        
    def store_decision(self, decision: Dict[str, Any]):
        """Store important organizational decisions"""
        decision_record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "context": decision.get("context", ""),
            "impact": decision.get("impact", ""),
            "decision_maker": decision.get("decision_maker", ""),
            "rationale": decision.get("rationale", "")
        }
        self.decisions_archive.append(decision_record)
    
    def store_lesson_learned(self, lesson: Dict[str, Any]):
        """Store lessons learned from projects or incidents"""
        lesson_record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "lesson": lesson,
            "category": lesson.get("category", "general"),
            "source_project": lesson.get("project", ""),
            "applicability": lesson.get("applicability", [])
        }
        self.lessons_learned.append(lesson_record)
    
    def store_best_practice(self, practice: Dict[str, Any]):
        """Store organizational best practices"""
        practice_record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "practice": practice,
            "department": practice.get("department", "organization"),
            "effectiveness_score": practice.get("effectiveness", 0.0),
            "implementation_guide": practice.get("implementation", "")
        }
        self.best_practices.append(practice_record)
    
    def log_event(self, event: Dict[str, Any]):
        """Log significant organizational events"""
        event_record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "type": event.get("type", "general"),
            "impact_level": event.get("impact", "medium"),
            "stakeholders": event.get("stakeholders", [])
        }
        self.organizational_events.append(event_record)
    
    def search_knowledge(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Search the organizational knowledge base"""
        results = []
        query_lower = query.lower()
        
        # Search decisions
        for decision in self.decisions_archive:
            if query_lower in json.dumps(decision).lower():
                results.append({"type": "decision", "content": decision})
        
        # Search lessons learned
        for lesson in self.lessons_learned:
            if query_lower in json.dumps(lesson).lower():
                if not category or lesson.get("category") == category:
                    results.append({"type": "lesson", "content": lesson})
        
        # Search best practices
        for practice in self.best_practices:
            if query_lower in json.dumps(practice).lower():
                results.append({"type": "best_practice", "content": practice})
        
        return results[:10]  # Return top 10 results
    
    def get_performance_trends(self, metric: str, time_period: int = 6) -> List[Dict[str, Any]]:
        """Get performance trends for specific metrics"""
        return self.performance_history.get(metric, [])[-time_period:]
    
    def update_performance_history(self, metrics: Dict[str, Any]):
        """Update performance history tracking"""
        timestamp = datetime.now().isoformat()
        for metric, value in metrics.items():
            if metric not in self.performance_history:
                self.performance_history[metric] = []
            
            self.performance_history[metric].append({
                "timestamp": timestamp,
                "value": value
            })
            
            # Keep only last 100 entries per metric
            if len(self.performance_history[metric]) > 100:
                self.performance_history[metric] = self.performance_history[metric][-100:]

class CommunicationSystem:
    """Manages all organizational communication and information flow"""
    
    def __init__(self):
        self.messages = []
        self.message_queues = {}  # Agent ID -> List[Message]
        self.organizational_memory = OrganizationalMemory()
        self.meeting_rooms = {}
        self.notification_system = NotificationSystem()
        
    def send_message(self, sender_id: str, receiver_id: str, message_type: MessageType, 
                    subject: str, content: str, priority: Priority = Priority.MEDIUM,
                    metadata: Dict[str, Any] = None) -> str:
        """Send a message between agents"""
        message = Message(
            id=str(uuid.uuid4()),
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_type=message_type,
            subject=subject,
            content=content,
            priority=priority,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        
        # Add to receiver's queue
        if receiver_id not in self.message_queues:
            self.message_queues[receiver_id] = []
        self.message_queues[receiver_id].append(message)
        
        # Send notification if high priority
        if priority.value >= Priority.HIGH.value:
            self.notification_system.send_notification(receiver_id, message)
        
        return message.id
    
    def get_messages(self, agent_id: str, unread_only: bool = False) -> List[Message]:
        """Get messages for a specific agent"""
        agent_messages = self.message_queues.get(agent_id, [])
        
        if unread_only:
            return [msg for msg in agent_messages if msg.read_at is None]
        
        return agent_messages
    
    def mark_message_read(self, message_id: str, reader_id: str) -> bool:
        """Mark a message as read"""
        for message in self.messages:
            if message.id == message_id and message.receiver_id == reader_id:
                message.read_at = datetime.now()
                return True
        return False
    
    def respond_to_message(self, original_message_id: str, response_content: str, 
                          sender_id: str) -> str:
        """Respond to a message"""
        original_message = None
        for msg in self.messages:
            if msg.id == original_message_id:
                original_message = msg
                break
        
        if not original_message:
            return None
        
        # Mark original as responded
        original_message.responded_at = datetime.now()
        
        # Send response
        response_id = self.send_message(
            sender_id=sender_id,
            receiver_id=original_message.sender_id,
            message_type=MessageType.GENERAL_COMMUNICATION,
            subject=f"Re: {original_message.subject}",
            content=response_content,
            priority=original_message.priority,
            metadata={"in_reply_to": original_message_id}
        )
        
        return response_id
    
    def broadcast_message(self, sender_id: str, recipient_ids: List[str], 
                         message_type: MessageType, subject: str, content: str,
                         priority: Priority = Priority.MEDIUM) -> List[str]:
        """Broadcast a message to multiple recipients"""
        message_ids = []
        for recipient_id in recipient_ids:
            msg_id = self.send_message(sender_id, recipient_id, message_type, 
                                     subject, content, priority)
            message_ids.append(msg_id)
        return message_ids
    
    def create_meeting(self, organizer_id: str, participant_ids: List[str], 
                      subject: str, agenda: str, scheduled_time: datetime) -> str:
        """Create a virtual meeting"""
        meeting_id = str(uuid.uuid4())
        meeting = {
            "id": meeting_id,
            "organizer": organizer_id,
            "participants": participant_ids,
            "subject": subject,
            "agenda": agenda,
            "scheduled_time": scheduled_time,
            "status": "scheduled",
            "transcript": [],
            "decisions": [],
            "action_items": []
        }
        
        self.meeting_rooms[meeting_id] = meeting
        
        # Send meeting invitations
        invitation_content = f"""
        Meeting Invitation: {subject}
        
        Organizer: {organizer_id}
        Scheduled Time: {scheduled_time}
        
        Agenda:
        {agenda}
        
        Please confirm your attendance.
        """
        
        for participant_id in participant_ids:
            self.send_message(
                sender_id=organizer_id,
                receiver_id=participant_id,
                message_type=MessageType.MEETING_REQUEST,
                subject=f"Meeting Invitation: {subject}",
                content=invitation_content,
                priority=Priority.MEDIUM,
                metadata={"meeting_id": meeting_id}
            )
        
        return meeting_id
    
    def conduct_meeting(self, meeting_id: str, duration_minutes: int = 60) -> Dict[str, Any]:
        """Simulate a meeting between agents"""
        if meeting_id not in self.meeting_rooms:
            return {"error": "Meeting not found"}
        
        meeting = self.meeting_rooms[meeting_id]
        meeting["status"] = "in_progress"
        meeting["start_time"] = datetime.now()
        
        # This would be expanded to actually facilitate agent communication
        # For now, we'll simulate a basic meeting outcome
        meeting_outcome = {
            "meeting_id": meeting_id,
            "duration": duration_minutes,
            "attendees": meeting["participants"],
            "decisions_made": [],
            "action_items": [],
            "next_steps": []
        }
        
        meeting["status"] = "completed"
        meeting["end_time"] = datetime.now()
        meeting["outcome"] = meeting_outcome
        
        # Store meeting in organizational memory
        self.organizational_memory.log_event({
            "type": "meeting",
            "meeting_id": meeting_id,
            "subject": meeting["subject"],
            "outcome": meeting_outcome
        })
        
        return meeting_outcome
    
    def get_communication_analytics(self, time_period_days: int = 30) -> Dict[str, Any]:
        """Get communication analytics and patterns"""
        cutoff_date = datetime.now()
        recent_messages = [
            msg for msg in self.messages 
            if (cutoff_date - msg.created_at).days <= time_period_days
        ]
        
        analytics = {
            "total_messages": len(recent_messages),
            "messages_by_type": {},
            "messages_by_priority": {},
            "response_rate": 0.0,
            "average_response_time": 0.0,
            "most_active_senders": {},
            "communication_patterns": {}
        }
        
        # Analyze message types
        for msg in recent_messages:
            msg_type = msg.message_type.value
            analytics["messages_by_type"][msg_type] = analytics["messages_by_type"].get(msg_type, 0) + 1
            
            priority = msg.priority.name
            analytics["messages_by_priority"][priority] = analytics["messages_by_priority"].get(priority, 0) + 1
            
            # Track sender activity
            analytics["most_active_senders"][msg.sender_id] = analytics["most_active_senders"].get(msg.sender_id, 0) + 1
        
        # Calculate response rate
        responded_messages = len([msg for msg in recent_messages if msg.responded_at])
        if recent_messages:
            analytics["response_rate"] = responded_messages / len(recent_messages)
        
        return analytics

class NotificationSystem:
    """Handles urgent notifications and alerts"""
    
    def __init__(self):
        self.notifications = []
        self.escalation_rules = {}
    
    def send_notification(self, agent_id: str, message: Message):
        """Send urgent notification to agent"""
        notification = {
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "message_id": message.id,
            "priority": message.priority,
            "timestamp": datetime.now(),
            "acknowledged": False
        }
        self.notifications.append(notification)
        
        # Handle escalation for critical messages
        if message.priority == Priority.CRITICAL:
            self._escalate_notification(notification)
    
    def _escalate_notification(self, notification: Dict[str, Any]):
        """Escalate critical notifications"""
        # Implementation for escalation logic
        # Could involve sending to multiple agents, triggering alerts, etc.
        pass
    
    def acknowledge_notification(self, notification_id: str) -> bool:
        """Acknowledge a notification"""
        for notif in self.notifications:
            if notif["id"] == notification_id:
                notif["acknowledged"] = True
                notif["acknowledged_at"] = datetime.now()
                return True
        return False

# Negotiation and Conflict Resolution System
class NegotiationSystem:
    """Handles negotiations and conflict resolution between agents"""
    
    def __init__(self, communication_system: CommunicationSystem):
        self.communication_system = communication_system
        self.active_negotiations = {}
        self.resolution_history = []
    
    def initiate_negotiation(self, initiator_id: str, other_party_id: str, 
                           topic: str, initial_proposal: Dict[str, Any]) -> str:
        """Start a negotiation between two agents"""
        negotiation_id = str(uuid.uuid4())
        
        negotiation = {
            "id": negotiation_id,
            "initiator": initiator_id,
            "other_party": other_party_id,
            "topic": topic,
            "status": "active",
            "proposals": [initial_proposal],
            "created_at": datetime.now(),
            "resolution": None
        }
        
        self.active_negotiations[negotiation_id] = negotiation
        
        # Send negotiation request
        self.communication_system.send_message(
            sender_id=initiator_id,
            receiver_id=other_party_id,
            message_type=MessageType.COLLABORATION_REQUEST,
            subject=f"Negotiation Request: {topic}",
            content=f"Proposal: {json.dumps(initial_proposal, indent=2)}",
            priority=Priority.HIGH,
            metadata={"negotiation_id": negotiation_id}
        )
        
        return negotiation_id
    
    def add_counter_proposal(self, negotiation_id: str, agent_id: str, 
                           proposal: Dict[str, Any]) -> bool:
        """Add a counter-proposal to an active negotiation"""
        if negotiation_id not in self.active_negotiations:
            return False
        
        negotiation = self.active_negotiations[negotiation_id]
        proposal["proposed_by"] = agent_id
        proposal["timestamp"] = datetime.now().isoformat()
        
        negotiation["proposals"].append(proposal)
        
        # Notify other party
        other_party = (negotiation["other_party"] if agent_id == negotiation["initiator"] 
                      else negotiation["initiator"])
        
        self.communication_system.send_message(
            sender_id=agent_id,
            receiver_id=other_party,
            message_type=MessageType.GENERAL_COMMUNICATION,
            subject=f"Counter-proposal: {negotiation['topic']}",
            content=f"New proposal: {json.dumps(proposal, indent=2)}",
            priority=Priority.HIGH,
            metadata={"negotiation_id": negotiation_id}
        )
        
        return True
    
    def resolve_negotiation(self, negotiation_id: str, resolution: Dict[str, Any]) -> bool:
        """Resolve a negotiation with agreed terms"""
        if negotiation_id not in self.active_negotiations:
            return False
        
        negotiation = self.active_negotiations[negotiation_id]
        negotiation["status"] = "resolved"
        negotiation["resolution"] = resolution
        negotiation["resolved_at"] = datetime.now()
        
        # Archive the negotiation
        self.resolution_history.append(negotiation)
        del self.active_negotiations[negotiation_id]
        
        # Notify both parties
        participants = [negotiation["initiator"], negotiation["other_party"]]
        for participant in participants:
            self.communication_system.send_message(
                sender_id="system",
                receiver_id=participant,
                message_type=MessageType.DECISION_NOTIFICATION,
                subject=f"Negotiation Resolved: {negotiation['topic']}",
                content=f"Resolution: {json.dumps(resolution, indent=2)}",
                priority=Priority.HIGH
            )
        
        return True 