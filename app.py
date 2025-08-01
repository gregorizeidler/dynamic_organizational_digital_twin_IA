import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
from datetime import datetime, timedelta
import time

from core.organizational_simulator import OrganizationalSimulator
from config import Config

# Configure Streamlit page
st.set_page_config(
    page_title="Organizational Digital Twin",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .agent-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .crisis-alert {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f44336;
    }
    .success-message {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_simulator():
    """Initialize the organizational simulator (cached)"""
    return OrganizationalSimulator()

def main():
    """Main application function"""
    
    # Initialize session state
    if 'simulator' not in st.session_state:
        st.session_state.simulator = initialize_simulator()
        st.session_state.auto_run = False
        st.session_state.simulation_speed = 1.0
    
    simulator = st.session_state.simulator
    
    # Header
    st.title("🏢 Organizational Digital Twin")
    st.markdown(f"**{Config.ORGANIZATION_NAME}** - Dynamic Simulation Environment")
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Simulation Controls")
        
        # Start/Stop simulation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start", disabled=simulator.is_running):
                simulator.start_simulation()
                st.rerun()
        
        with col2:
            if st.button("⏹️ Stop", disabled=not simulator.is_running):
                simulator.stop_simulation()
                st.rerun()
        
        # Auto-run controls
        st.session_state.auto_run = st.checkbox("🔄 Auto-run simulation", value=st.session_state.auto_run)
        st.session_state.simulation_speed = st.slider("Simulation Speed", 0.5, 5.0, st.session_state.simulation_speed, 0.5)
        
        # Manual day advancement
        if st.button("⏭️ Advance Day", disabled=not simulator.is_running):
            day_result = simulator.simulate_day()
            st.success(f"Day {simulator.simulation_day} completed!")
            st.rerun()
        
        st.divider()
        
        # Crisis simulation
        st.subheader("⚠️ Crisis Simulation")
        crisis_type = st.selectbox("Crisis Type", ["data_breach", "major_competitor", "key_employee_departure"])
        
        if st.button("🚨 Trigger Crisis"):
            crisis_result = simulator.inject_crisis(crisis_type)
            st.error(f"Crisis triggered: {crisis_type}")
            st.json(crisis_result)
        
        st.divider()
        
        # Simulation info
        st.subheader("ℹ️ Simulation Info")
        st.write(f"**Day:** {simulator.simulation_day}")
        st.write(f"**Status:** {'🟢 Running' if simulator.is_running else '🔴 Stopped'}")
        st.write(f"**Agents:** {len(simulator.agents)}")
        st.write(f"**Messages:** {len(simulator.communication_system.messages)}")
    
    # Main content area
    if not simulator.is_running:
        show_welcome_screen()
    else:
        show_simulation_dashboard(simulator)
    
    # Auto-run simulation
    if st.session_state.auto_run and simulator.is_running:
        time.sleep(1 / st.session_state.simulation_speed)
        day_result = simulator.simulate_day()
        st.rerun()

def show_welcome_screen():
    """Show welcome screen when simulation is not running"""
    st.markdown("""
    ## Welcome to the Organizational Digital Twin Simulation
    
    This advanced simulation creates a complete digital replica of a tech startup organization, 
    featuring autonomous AI agents that represent different roles within the company.
    
    ### 🎯 Key Features:
    - **Autonomous Agents**: CEO, CFO, CTO, CMO, and HR Director with realistic decision-making
    - **Market Simulation**: Dynamic market conditions and competitor actions
    - **Communication System**: Inter-agent messaging and negotiation
    - **Organizational Memory**: Learning from past decisions and experiences
    - **Performance Metrics**: Real-time tracking of company performance
    
    ### 🚀 Getting Started:
    1. Click "Start" in the sidebar to begin the simulation
    2. Watch as agents interact and make decisions autonomously
    3. Use "Auto-run" for continuous simulation or advance manually
    4. Trigger crisis scenarios to test organizational resilience
    
    **Click "Start" to begin your organizational simulation journey!**
    """)
    
    # Show initial configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Initial Budget", f"${Config.INITIAL_BUDGET:,}")
    
    with col2:
        st.metric("Market Size", f"${Config.MARKET_SIZE:,}")
    
    with col3:
        st.metric("Simulation Cycle", f"{Config.SIMULATION_CYCLE_DAYS} days")

def show_simulation_dashboard(simulator):
    """Show the main simulation dashboard"""
    
    # Get current status
    status = simulator.get_simulation_status()
    
    # Performance metrics header
    st.header("📊 Performance Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Market Share", 
            f"{status['performance_metrics']['market_share']:.2%}",
            delta=f"{status['performance_metrics']['market_share'] - 0.01:.2%}"
        )
    
    with col2:
        revenue = status['performance_metrics']['revenue']
        st.metric(
            "Revenue",
            f"${revenue:,.0f}",
            delta=f"${revenue * 0.1:,.0f}"
        )
    
    with col3:
        profit_margin = status['performance_metrics']['profit_margin']
        st.metric(
            "Profit Margin",
            f"{profit_margin:.1%}",
            delta=f"{profit_margin * 0.1:.1%}"
        )
    
    with col4:
        satisfaction = status['performance_metrics']['customer_satisfaction']
        st.metric(
            "Customer Satisfaction",
            f"{satisfaction:.1%}",
            delta=f"{(satisfaction - 0.5) * 0.1:.1%}"
        )
    
    with col5:
        innovation = status['performance_metrics']['innovation_index']
        st.metric(
            "Innovation Index",
            f"{innovation:.2f}",
            delta=f"{(innovation - 0.5) * 0.1:.2f}"
        )
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Organization", "📈 Performance", "💬 Communications", 
        "🌍 Market", "📋 Events"
    ])
    
    with tab1:
        show_organization_tab(simulator, status)
    
    with tab2:
        show_performance_tab(simulator, status)
    
    with tab3:
        show_communications_tab(simulator, status)
    
    with tab4:
        show_market_tab(simulator, status)
    
    with tab5:
        show_events_tab(simulator, status)

def show_organization_tab(simulator, status):
    """Show organization structure and agent status"""
    st.subheader("👥 Agent Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        for agent_id in ["ceo", "cfo", "cto"]:
            if agent_id in status['agent_status']:
                agent_data = status['agent_status'][agent_id]
                with st.container():
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4>{agent_data['role']} - {agent_data['name']}</h4>
                        <p><strong>Department:</strong> {agent_data['department']}</p>
                        <p><strong>Workload:</strong> {agent_data['workload']}</p>
                        <p><strong>Tasks Completed:</strong> {agent_data['completed_tasks']}</p>
                        <p><strong>Efficiency:</strong> {agent_data['efficiency_score']:.1%}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        for agent_id in ["cmo", "hr"]:
            if agent_id in status['agent_status']:
                agent_data = status['agent_status'][agent_id]
                with st.container():
                    st.markdown(f"""
                    <div class="agent-card">
                        <h4>{agent_data['role']} - {agent_data['name']}</h4>
                        <p><strong>Department:</strong> {agent_data['department']}</p>
                        <p><strong>Workload:</strong> {agent_data['workload']}</p>
                        <p><strong>Tasks Completed:</strong> {agent_data['completed_tasks']}</p>
                        <p><strong>Efficiency:</strong> {agent_data['efficiency_score']:.1%}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Organization chart
    st.subheader("📊 Organization Chart")
    
    # Create organizational hierarchy visualization
    fig = go.Figure()
    
    # Add CEO at the top
    fig.add_trace(go.Scatter(
        x=[2], y=[3],
        mode='markers+text',
        marker=dict(size=50, color='#ff7f0e'),
        text=['CEO'],
        textposition="middle center",
        name='Executive'
    ))
    
    # Add C-level executives
    positions = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
    roles = ['CFO', 'CTO', 'CMO', 'HR', 'COO']
    
    for i, (x, y) in enumerate(positions[:4]):  # Only show the agents we have
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=40, color='#1f77b4'),
            text=[roles[i]],
            textposition="middle center",
            showlegend=False
        ))
    
    # Add connecting lines
    for x, y in positions[:4]:
        fig.add_trace(go.Scatter(
            x=[2, x], y=[3, y],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False
        ))
    
    fig.update_layout(
        title="Organizational Structure",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=300,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_performance_tab(simulator, status):
    """Show performance metrics and trends"""
    st.subheader("📈 Performance Trends")
    
    # Get performance history
    memory = simulator.communication_system.organizational_memory
    
    # Create performance trends chart
    metrics_to_plot = ['market_share', 'revenue', 'customer_satisfaction', 'innovation_index']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Market Share', 'Revenue', 'Customer Satisfaction', 'Innovation Index'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    for i, metric in enumerate(metrics_to_plot):
        row = (i // 2) + 1
        col = (i % 2) + 1
        
        # Get trend data
        trend_data = memory.get_performance_trends(metric, time_period=10)
        
        if trend_data:
            dates = [datetime.fromisoformat(d['timestamp']) for d in trend_data]
            values = [d['value'] for d in trend_data]
            
            fig.add_trace(
                go.Scatter(x=dates, y=values, mode='lines+markers', name=metric),
                row=row, col=col
            )
        else:
            # Show current value if no history
            current_value = status['performance_metrics'].get(metric, 0)
            fig.add_trace(
                go.Scatter(x=[datetime.now()], y=[current_value], mode='markers', name=metric),
                row=row, col=col
            )
    
    fig.update_layout(height=600, showlegend=False, title_text="Performance Metrics Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Current Objectives")
        ceo = simulator.agents.get("ceo")
        if ceo and hasattr(ceo, 'okrs') and ceo.okrs:
            for okr in ceo.okrs:
                st.write(f"**{okr['objective']}**")
                for kr in okr['key_results']:
                    st.write(f"  • {kr}")
        else:
            st.write("No OKRs set yet")
    
    with col2:
        st.subheader("💰 Financial Health")
        cfo = simulator.agents.get("cfo")
        if cfo and hasattr(cfo, 'cash_flow'):
            cash_flow = cfo.cash_flow
            st.metric("Cash Balance", f"${cash_flow['current_balance']:,}")
            st.metric("Monthly Burn", f"${cash_flow['monthly_burn_rate']:,}")
            st.metric("Runway", f"{cash_flow['runway_months']:.1f} months")

def show_communications_tab(simulator, status):
    """Show communication analytics and recent messages"""
    st.subheader("💬 Communication Analytics")
    
    analytics = status['communication_analytics']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Messages", analytics['total_messages'])
    
    with col2:
        st.metric("Response Rate", f"{analytics['response_rate']:.1%}")
    
    with col3:
        st.metric("Active Negotiations", status['active_negotiations'])
    
    # Message type distribution
    if analytics['messages_by_type']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Messages by Type")
            df_msg_type = pd.DataFrame(
                list(analytics['messages_by_type'].items()),
                columns=['Type', 'Count']
            )
            fig = px.pie(df_msg_type, values='Count', names='Type', title="Message Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚡ Messages by Priority")
            df_priority = pd.DataFrame(
                list(analytics['messages_by_priority'].items()),
                columns=['Priority', 'Count']
            )
            fig = px.bar(df_priority, x='Priority', y='Count', title="Priority Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent messages
    st.subheader("📨 Recent Communications")
    
    recent_messages = simulator.communication_system.messages[-10:]  # Last 10 messages
    
    if recent_messages:
        for msg in reversed(recent_messages):
            priority_color = {
                'LOW': '#4caf50',
                'MEDIUM': '#ff9800', 
                'HIGH': '#f44336',
                'URGENT': '#9c27b0',
                'CRITICAL': '#d32f2f'
            }.get(msg.priority.name, '#757575')
            
            st.markdown(f"""
            <div style="border-left: 4px solid {priority_color}; padding: 1rem; margin: 0.5rem 0; background-color: #f9f9f9;">
                <strong>{msg.sender_id} → {msg.receiver_id}</strong> ({msg.priority.name})<br>
                <strong>{msg.subject}</strong><br>
                <small>{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No messages yet")

def show_market_tab(simulator, status):
    """Show market conditions and competitor analysis"""
    st.subheader("🌍 Market Conditions")
    
    market_conditions = status['market_conditions']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Market Size", f"${market_conditions['market_size']:,.0f}")
        st.metric("Growth Rate", f"{market_conditions['growth_rate']:.1%}")
    
    with col2:
        st.metric("Competition Intensity", f"{market_conditions['competition_intensity']:.1%}")
        st.metric("Customer Sentiment", f"{market_conditions['customer_sentiment']:.1%}")
    
    with col3:
        st.write("**Economic Conditions:**")
        st.write(market_conditions['economic_conditions'].title())
        st.write("**Regulatory Environment:**")
        st.write(market_conditions['regulatory_environment'].title())
    
    # Technology trends
    st.subheader("💡 Technology Trends")
    trends = market_conditions.get('technology_trends', [])
    for trend in trends:
        st.write(f"• {trend}")
    
    # Competitor analysis
    st.subheader("🏆 Competitive Landscape")
    
    competitors = simulator.market_simulator.competitors
    if competitors:
        df_competitors = pd.DataFrame(competitors)
        
        # Market share pie chart
        fig = px.pie(
            df_competitors, 
            values='market_share', 
            names='name',
            title="Market Share Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Competitor details
        st.subheader("📊 Competitor Details")
        st.dataframe(df_competitors[['name', 'market_share', 'strategy', 'product_quality']])

def show_events_tab(simulator, status):
    """Show recent events and simulation log"""
    st.subheader("📋 Recent Events")
    
    recent_events = status['recent_events']
    
    if recent_events:
        for day_log in reversed(recent_events):
            with st.expander(f"Day {day_log['day']} - {len(day_log['events'])} events"):
                
                # Events
                if day_log['events']:
                    st.write("**Events:**")
                    for event in day_log['events']:
                        event_type = event.get('type', 'unknown')
                        
                        if event_type == 'morning_briefing':
                            st.info(f"📊 Morning briefing generated")
                        elif event_type == 'task_completion':
                            st.success(f"✅ {event['agent']} completed: {event['task']}")
                        elif event_type == 'market_update':
                            st.warning(f"🌍 Market update: {len(event['data']['market_events'])} events")
                        elif event_type == 'spontaneous_activity':
                            st.write(f"🎯 {event['agent']}: {event['activity']}")
                        else:
                            st.write(f"📝 {event_type}: {event}")
                
                # Communications
                if day_log['communications']:
                    st.write("**Communications:**")
                    for comm in day_log['communications']:
                        if comm['type'] == 'inter_agent_communication':
                            st.write(f"💬 {comm['sender']} → {comm['receiver']}: {comm['topic']}")
                        elif comm['type'] == 'negotiation_initiated':
                            st.write(f"🤝 Negotiation: {comm['topic']} ({', '.join(comm['parties'])})")
                
                # Performance
                if day_log['performance']:
                    st.write("**Performance:**")
                    perf = day_log['performance']
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"Market Share: {perf['market_share']:.2%}")
                    with col2:
                        st.write(f"Revenue: ${perf['revenue']:,.0f}")
                    with col3:
                        st.write(f"Satisfaction: {perf['customer_satisfaction']:.1%}")
    else:
        st.write("No events recorded yet. Start the simulation to see activity!")
    
    # Organizational memory insights
    st.subheader("🧠 Organizational Memory")
    
    memory = simulator.communication_system.organizational_memory
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Decisions Archived", len(memory.decisions_archive))
    
    with col2:
        st.metric("Lessons Learned", len(memory.lessons_learned))
    
    with col3:
        st.metric("Best Practices", len(memory.best_practices))

if __name__ == "__main__":
    main() 