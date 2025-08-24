import streamlit as st
import requests
from datetime import datetime
import pytz

# Configuration
API_BASE_URL = "https://dev.pulse-api.getpulseinsights.ai"

def format_timestamp(timestamp_str):
    """Format timestamp to relative time (e.g., '2 minutes ago')"""
    try:
        # Parse the timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # Convert to local timezone
        local_tz = pytz.timezone('UTC')  # You can change this to your local timezone
        dt = dt.astimezone(local_tz)
        
        # Calculate time difference
        now = datetime.now(local_tz)
        diff = now - dt
        
        if diff.days > 0:
            if diff.days == 1:
                return "1 day ago"
            else:
                return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            if hours == 1:
                return "1 hour ago"
            else:
                return f"{hours} hours ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            if minutes == 1:
                return "1 minute ago"
            else:
                return f"{minutes} minutes ago"
        else:
            return "Just now"
    except:
        return "Unknown time"

def get_memories(org_id, page=1, page_size=15):
    """Fetch memories from the API"""
    try:
        headers = {"x-org-id": org_id}
        url = f"{API_BASE_URL}/api/memories"
        params = {"page": page, "page_size": page_size}
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch memories: {response.status_code}")
            st.error(f"Response: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error fetching memories: {str(e)}")
        return None

def render_memory_card(memory, index):
    """Render a single memory card using Streamlit native components"""
    # Extract memory data
    title = memory.get('title', 'Untitled Memory')
    summary = memory.get('summary', 'No summary available')
    created_at = memory.get('created_at', '')
    
    # Format timestamp
    time_ago = format_timestamp(created_at)
    
    # Create icon based on memory type or use default
    icon_map = {
        'meeting': '📅',
        'email': '📧',
        'document': '📄',
        'conversation': '💬',
        'decision': '✅',
        'note': '📝'
    }
    
    # Try to determine icon from title or summary
    icon = '🧠'  # Default brain icon
    for key, emoji in icon_map.items():
        if key.lower() in title.lower() or key.lower() in summary.lower():
            icon = emoji
            break
    
    # Create the memory card using a single HTML structure
    st.markdown(f"""
    <div class="memory-card">
        <div style="display: flex; align-items: flex-start; gap: 1rem;">
            <div class="memory-icon">{icon}</div>
            <div style="flex: 1; min-width: 0;">
                <div class="memory-title">{title}</div>
                <div class="memory-summary">{summary}</div>
                <div style="margin-top: 1rem;">
                    <div class="memory-timestamp">🕒 {time_ago}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def intakes_history_tab():
    """Main function for the Intakes History tab"""
    # Add custom CSS for better card styling
    st.markdown("""
    <style>
    .memory-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .memory-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .memory-icon {
        background: var(--primary-light);
        color: var(--primary);
        width: 48px;
        height: 48px;
        border-radius: var(--radius);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-top: 0.5rem;
        flex-shrink: 0;
    }
    
    .memory-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .memory-summary {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .memory-timestamp {
        color: var(--text-muted);
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    /* Control alignment and button styling */
    .stButton > button {
        height: 38px !important;
        border-radius: var(--radius-lg) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:disabled {
        background: var(--bg-tertiary) !important;
        color: var(--text-muted) !important;
        border: 1px solid var(--border-light) !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    
    .stButton > button:disabled:hover {
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <h2>Intakes History</h2>
            <p>View all memories captured by Scooby AI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get organization ID from session state or use a default
    org_id = st.session_state.get("org_id", "832697dd-a913-405d-907a-a0c177d0746f")
    
    # Pagination controls
    page_size = st.selectbox(
        "Items per page",
        options=[5, 10, 15, 25],
        index=0,  # Default to 2
        key="page_size_selector"
    )
    
    # Initialize current page in session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1
    
    # Fetch memories
    with st.spinner("Loading memories..."):
        memories_data = get_memories(org_id, page=st.session_state.current_page, page_size=page_size)
    
    if memories_data:
        # Parse the correct response structure
        memories = memories_data.get('memories', [])
        pagination = memories_data.get('pagination', {})
        total_count = pagination.get('total_count', 0)
        current_page = pagination.get('page', 1)
        total_pages = pagination.get('total_pages', 1)
        has_next = pagination.get('has_next', False)
        has_prev = pagination.get('has_prev', False)
        
        # Update session state with current page from API
        st.session_state.current_page = current_page
        
        # Pagination buttons in a row
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Refresh", key="refresh_memories", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("Previous", key="prev_page", use_container_width=True, disabled=not has_prev):
                st.session_state.current_page = max(1, current_page - 1)
                st.rerun()
        
        with col3:
            if st.button("Next", key="next_page", use_container_width=True, disabled=not has_next):
                st.session_state.current_page = current_page + 1
                st.rerun()
        
        if memories:
            # Display pagination info
            st.markdown(f"""
            <div style="
                background: var(--bg-tertiary);
                border: 1px solid var(--border-light);
                border-radius: var(--radius);
                padding: 1rem;
                margin-bottom: 1.5rem;
                text-align: center;
            ">
                <span style="color: var(--text-secondary); font-size: 0.875rem;">
                    Page {current_page} of {total_pages} • Showing {len(memories)} of {total_count} memories
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Render each memory
            for i, memory in enumerate(memories):
                render_memory_card(memory, i)
                
                # Add some spacing between cards
                if i < len(memories) - 1:
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                text-align: center;
                padding: 3rem 1rem;
                color: var(--text-muted);
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                <h3 style="color: var(--text-secondary); margin-bottom: 0.5rem;">No memories yet</h3>
                <p style="margin: 0;">Scooby hasn't captured any memories yet. Start using the Data Intake & Management tab to create some!</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 3rem 1rem;
            color: var(--text-muted);
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
            <h3 style="color: var(--text-secondary); margin-bottom: 0.5rem;">Unable to load memories</h3>
            <p style="margin: 0;">There was an error connecting to the API. Please check your connection and try again.</p>
        </div>
        """, unsafe_allow_html=True)
