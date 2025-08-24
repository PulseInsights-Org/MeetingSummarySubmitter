import streamlit as st
import requests
import uuid
import time
import json
from typing import Optional
from supabase import create_client, Client

# Configuration
API_BASE_URL = "https://dev.pulse-api.getpulseinsights.ai"
API_BOT_URL = "https://pulse-dev.scooby.getpulseinsights.ai"

# Supabase Configuration
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "your-supabase-url")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY", "your-supabase-anon-key")

@st.cache_resource
def init_supabase() -> Client:
    """Initialize Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def load_modern_css():
    """Load clean, professional CSS with minimal design"""
    st.markdown("""
    <style>
    /* Import clean fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Color System */
    :root {
        /* Light theme colors */
        --primary: #2563eb;
        --primary-hover: #1d4ed8;
        --primary-light: #dbeafe;
        --primary-dark: #1e40af;
        
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-400: #9ca3af;
        --gray-500: #6b7280;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;
        
        --success: #10b981;
        --success-light: #d1fae5;
        --warning: #f59e0b;
        --warning-light: #fef3c7;
        --error: #ef4444;
        --error-light: #fee2e2;
        
        --bg-primary: #ffffff;
        --bg-secondary: #f9fafb;
        --bg-tertiary: #f3f4f6;
        --text-primary: #111827;
        --text-secondary: #374151;
        --text-muted: #6b7280;
        --border: #e5e7eb;
        --border-light: #f3f4f6;
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        
        --radius-sm: 4px;
        --radius: 6px;
        --radius-lg: 8px;
        --radius-xl: 12px;
    }
    
    /* Dark theme */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #111827;
            --bg-secondary: #1f2937;
            --bg-tertiary: #374151;
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --text-muted: #9ca3af;
            --border: #374151;
            --border-light: #4b5563;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px 0 rgba(0, 0, 0, 0.2);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
        }
    }
    
    /* Base styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none !important; }
    .stToolbar { display: none !important; }
    
    /* Login Page */
    .login-container {
        max-width: 400px;
        margin: 4rem auto;
        padding: 3rem;
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-lg);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    
    .login-subtitle {
        color: var(--text-muted);
        font-size: 1rem;
        margin: 0;
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-lg) !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        height: auto !important;
    }
    
    .stButton > button:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Secondary button */
    .secondary-btn > button {
        background: var(--bg-secondary) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border) !important;
    }
    
    .secondary-btn > button:hover {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
    }
    
    /* App Header */
    .app-header {
        background: var(--bg-primary);
        border-bottom: 1px solid var(--border);
        padding: 1.5rem 0;
        margin-bottom: 2rem;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .brand-section h1 {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    
    .brand-section p {
        color: var(--text-muted);
        font-size: 0.875rem;
        margin: 0.25rem 0 0 0;
    }
    
    .user-section {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.5rem 1rem;
        background: var(--bg-secondary);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        background: var(--primary);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .user-info h4 {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .user-info p {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Cards */
    .card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-sm);
    }
    
    .card-header {
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-light);
    }
    
    .card-header h2 {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    
    .card-header p {
        color: var(--text-muted);
        font-size: 0.875rem;
        margin: 0;
    }
    
    /* Status indicator */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--success-light);
        color: var(--success);
        padding: 0.5rem 1rem;
        border-radius: var(--radius-lg);
        font-size: 0.875rem;
        font-weight: 500;
        border: 1px solid var(--success);
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        background: var(--success);
        border-radius: 50%;
    }
    
    /* Metrics */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0 0 0.25rem 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    /* Response section */
    .response-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .response-header {
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary);
        margin: 0 0 1rem 0;
    }
    
    .query-preview {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-light);
        border-radius: var(--radius);
        padding: 0.75rem;
        margin-bottom: 1rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-style: italic;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: var(--radius-lg);
        padding: 0.25rem;
        border: 1px solid var(--border);
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: var(--radius);
        color: var(--text-muted);
        font-weight: 500;
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary);
        color: white;
        font-weight: 600;
    }
    
    /* File uploader */
    .stFileUploader {
        background: var(--bg-secondary);
        border: 2px dashed var(--border);
        border-radius: var(--radius-lg);
        padding: 2rem 1rem;
        text-align: center;
    }
    
    .stFileUploader:hover {
        border-color: var(--primary);
        background: var(--primary-light);
    }
    
    /* Alert messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: var(--radius-lg);
        border: none;
        padding: 0.75rem 1rem;
        font-size: 0.875rem;
    }
    
    .stSuccess {
        background: var(--success-light);
        color: var(--success);
    }
    
    .stError {
        background: var(--error-light);
        color: var(--error);
    }
    
    .stWarning {
        background: var(--warning-light);
        color: var(--warning);
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: var(--radius-xl);
        color: var(--text-muted);
    }
    
    .empty-state h3 {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin: 0 0 0.5rem 0;
    }
    
    .empty-state p {
        font-size: 0.875rem;
        margin: 0 0 1.5rem 0;
    }
    
    /* Section divider */
    .section-divider {
        margin: 3rem 0 2rem 0;
        border: none;
        border-top: 2px solid var(--border);
        position: relative;
    }
    
    .section-divider::after {
        content: '';
        position: absolute;
        top: -1px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 2px;
        background: var(--primary);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .login-container {
            margin: 2rem 1rem;
            padding: 2rem;
        }
        
        .header-content {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
        }
        
        .user-section {
            flex-direction: column;
        }
        
        .card {
            padding: 1.5rem;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Override Streamlit defaults */
    div[data-testid="stMarkdownContainer"] p {
        color: var(--text-primary);
    }
    
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {
        color: var(--text-primary);
    }
    
    .stTextInput > label,
    .stTextArea > label,
    .stFileUploader > label {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.875rem;
    }
    </style>
    """, unsafe_allow_html=True)

def authenticate_user(org_name: str, password: str) -> tuple[bool, Optional[str]]:
    """Authenticate user with org_name and password against Supabase"""
    try:
        if not org_name or not password:
            return False, None
            
        supabase = init_supabase()
        response = supabase.table("orgs").select("id, org_name, password").eq("org_name", org_name).execute()
        
        if not response.data:
            st.error("Organization not found")
            return False, None
        
        org_data = response.data[0]
        
        if org_data["password"] == password:
            return True, org_data["id"]
        else:
            st.error("Invalid password")
            return False, None
            
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False, None

def login_page():
    """Display the clean login page"""
    st.set_page_config(
        page_title="Pulse Copilot - Sign In",
        page_icon="⚡",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    load_modern_css()
    
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h1 class="login-title">Pulse Copilot</h1>
            <p class="login-subtitle">Sign in to access your AI-powered insights platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Login form
    with st.form("login_form", clear_on_submit=False):
        org_name = st.text_input(
            "Organization Name",
            placeholder="Enter your organization name",
            key="org_name_input"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="password_input"
        )
        
        submitted = st.form_submit_button("Sign In", use_container_width=True)
        
        if submitted:
            if not org_name or not password:
                st.error("Please enter both organization name and password")
            else:
                with st.spinner("Authenticating..."):
                    supabase = init_supabase()
                    is_authenticated, org_id = authenticate_user(org_name, password)
                    tenant_id = supabase.table("org_directory").select("tenant_id").eq("org_id", org_id).execute()
                    if is_authenticated:
                        st.session_state.authenticated = True
                        st.session_state.org_name = org_name
                        st.session_state.org_id = org_id
                        st.session_state.tenant_id = tenant_id
                        st.session_state.password = password
                        st.success("Login successful! Redirecting...")
                        time.sleep(1)
                        st.rerun()

def generate_idempotency_key():
    """Generate a unique idempotency key"""
    return str(uuid.uuid4())

def get_or_create_idempotency_key():
    """Get existing idempotency key or create a new one"""
    if "idempotency_key" not in st.session_state or st.session_state.idempotency_key is None:
        st.session_state.idempotency_key = generate_idempotency_key()
    return st.session_state.idempotency_key

def init_intake() -> Optional[str]:
    """Initialize a new intake and return the intake_id"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "x-idempotency-key": get_or_create_idempotency_key(),
            "Authorization": f"Bearer {st.session_state.password}"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/intakes/init", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("intake_id")
        else:
            st.error(f"Failed to initialize intake: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error initializing intake: {str(e)}")
        return None

def upload_file(intake_id: str, uploaded_file) -> bool:
    """Upload a file to the intake"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "x-idempotency-key": get_or_create_idempotency_key(),
            "Authorization": f"Bearer {st.session_state.password}"
        }
        
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        response = requests.post(f"{API_BASE_URL}/api/upload/file/{intake_id}", headers=headers, files=files)
        
        if response.status_code == 200:
            st.success("File uploaded successfully!")
            st.session_state.idempotency_key = generate_idempotency_key()
            return True
        else:
            st.error(f"Failed to upload file: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return False

def upload_text(intake_id: str, text_content: str) -> bool:
    """Upload text content to the intake"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "x-idempotency-key": get_or_create_idempotency_key(),
            "Authorization": f"Bearer {st.session_state.password}"
        }
        
        data = {"text_content": text_content}
        
        response = requests.post(f"{API_BASE_URL}/api/upload/text/{intake_id}", headers=headers, data=data)
        
        if response.status_code == 200:
            st.success("Text uploaded successfully!")
            st.session_state.idempotency_key = generate_idempotency_key()
            return True
        else:
            st.error(f"Failed to upload text: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error uploading text: {str(e)}")
        return False

def get_intake_status(intake_id: str) -> Optional[dict]:
    """Get the status of an intake"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "Authorization": f"Bearer {st.session_state.password}"
        }
        
        response = requests.get(f"{API_BASE_URL}/api/intakes/{intake_id}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get intake status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error getting intake status: {str(e)}")
        return None

def query_insights(query: str) -> Optional[dict]:
    """Query insights from the API using the /api/query endpoint"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "Content-Type": "application/json"
        }
        
        data = {"question": query}  
        
        response = requests.post(f"{API_BASE_URL}/api/query", headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to query insights: {response.status_code}")
            if response.text:
                st.error(f"Response: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error querying insights: {str(e)}")
        return None

def add_scooby_to_meeting(meeting_link: str) -> bool:
    """Add Scooby to the meeting using the provided endpoint"""
    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.org_id}",
            "Content-Type": "application/json"
        }
        
        data = {
            "meeting_url": meeting_link,
            "x_org_id": str(st.session_state.org_id) if st.session_state.org_id else "",
            "tenant_id": str(st.session_state.tenant_id) if st.session_state.tenant_id else "",
            "isTranscript": True,
            "saveTranscript": True
        }
        
        response = requests.post(f"{API_BOT_URL}/add_scooby", headers=headers, json=data)
        
        if response.status_code == 200:
            st.success("Scooby has been successfully added to your meeting!")
            return True
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            st.error(f"Failed to add Scooby to meeting: {response.status_code}\n{error_data}")
            return False
    except Exception as e:
        st.error(f"Error adding Scooby to meeting: {str(e)}")
        return False

def finalize_intake(intake_id: str) -> bool:
    """Finalize the intake"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "Authorization": f"Bearer {st.session_state.password}"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/intakes/{intake_id}/finalize", headers=headers)
        
        if response.status_code == 200:
            st.success("Intake finalized successfully!")
            return True
        else:
            st.error(f"Failed to finalize intake: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error finalizing intake: {str(e)}")
        return False

def reset_session():
    """Reset the session and clear all state"""
    st.session_state.intake_id = None
    st.session_state.intake_initialized = False
    st.session_state.idempotency_key = None
    if hasattr(st.session_state, 'last_query_response'):
        delattr(st.session_state, 'last_query_response')
    st.success("Session reset successfully!")
    st.rerun()

def logout():
    """Logout and clear authentication"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()

def main_app():
    """Main application with clean, professional design"""
    st.set_page_config(
        page_title="Pulse Copilot - Dashboard",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    load_modern_css()
    
    # Clean Header
    org_initial = st.session_state.org_name[0].upper() if st.session_state.org_name else "O"
    
    st.markdown(f"""
    <div class="app-header">
        <div class="header-content">
            <div class="brand-section">
                <h1>Pulse Copilot</h1>
            </div>
            <div class="user-section">
                <div class="user-avatar">{org_initial}</div>
                <div class="user-info">
                    <h4>{st.session_state.org_name}</h4>
                    <p>ID: {st.session_state.org_id}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2, col3 = st.columns([6, 1, 2])
    with col3:
        if st.button("Sign Out", key="logout_btn", use_container_width=True):
            logout()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize session state
    if "intake_id" not in st.session_state:
        st.session_state.intake_id = None
    if "intake_initialized" not in st.session_state:
        st.session_state.intake_initialized = False
    if "idempotency_key" not in st.session_state:
        st.session_state.idempotency_key = None
    
    # Clean tabs - now with merged Data Intake & Management tab
    tab1, tab2, tab3 = st.tabs(["Data Intake & Management", "Query Insights", "Meeting Assistant"])
    
    with tab1:
        # Step 1: Initialize Intake
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <h2>Initialize Intake Session</h2>
                <p>Start a new session to upload your meetings transcript to Pulse</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Initialize New Intake", key="init_btn", use_container_width=True):
                with st.spinner("Initializing intake session..."):
                    intake_id = init_intake()
                    if intake_id:
                        st.session_state.intake_id = intake_id
                        st.session_state.intake_initialized = True
                        st.success("Intake session initialized successfully!")
        
        if st.session_state.intake_initialized:
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <div class="status-badge">
                    <div class="status-dot"></div>
                    Active Session: {st.session_state.intake_id[:8]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Step 2: Upload Content
        if st.session_state.intake_initialized:
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h2>Upload Your Content</h2>
                    <p>Add documents, files, or text content to Pulse</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            upload_tab1, upload_tab2 = st.tabs(["File Upload", "Text Input"])
            
            with upload_tab1:
                st.markdown("#### Upload Documents")
                st.write("Upload files containing your meeting notes, reports, research, or any text content.")
                
                uploaded_file = st.file_uploader(
                    "Choose a file",
                    type=["txt", "md", "pdf", "docx"],
                    help="Supported formats: .txt, .md, .pdf, .docx (Max 10MB)",
                    label_visibility="collapsed"
                )
                
                if uploaded_file is not None:
                    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">File Name</div>
                            <div style="font-weight: 600; color: var(--text-primary); font-size: 0.9rem; margin-top: 0.5rem; word-break: break-all;">
                                {uploaded_file.name}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        file_size_mb = uploaded_file.size / (1024 * 1024)
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{file_size_mb:.1f}</div>
                            <div class="metric-label">MB</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{uploaded_file.type.split('/')[-1].upper()}</div>
                            <div class="metric-label">Format</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("Upload File", key="upload_file_btn", use_container_width=True):
                            with st.spinner("Uploading and processing your file..."):
                                if upload_file(st.session_state.intake_id, uploaded_file):
                                    st.rerun()
            
            with upload_tab2:
                st.markdown("#### Direct Text Input")
                st.write("Enter your content directly for immediate analysis and processing.")
                
                text_content = st.text_area(
                    "Content",
                    placeholder="Paste your meeting notes, research findings, reports, or any text content here...\n\nExample:\n- Meeting summary from Q4 planning session\n- Customer feedback analysis\n- Project status reports\n- Research findings",
                    height=300,
                    help="Enter any text content you'd like to analyze",
                    label_visibility="collapsed"
                )
                
                if text_content.strip():
                    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{len(text_content):,}</div>
                            <div class="metric-label">Characters</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        word_count = len(text_content.split())
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{word_count:,}</div>
                            <div class="metric-label">Words</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        estimated_read_time = max(1, word_count // 200)
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{estimated_read_time}</div>
                            <div class="metric-label">Min Read</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("Upload Text", key="upload_text_btn", use_container_width=True):
                            with st.spinner("Processing and analyzing your text..."):
                                if upload_text(st.session_state.intake_id, text_content):
                                    st.rerun()
            
            # Management Section - Divider
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            
            # Management Section
            st.markdown("""
            <div class="card">
                <div class="card-header">
                    <h2>Session Management</h2>
                    <p>Manage your current intake session and finalize your data to add it to the Pulse knowledge base</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Current session info
            st.markdown(f"""
            <div style="background: var(--bg-secondary); 
                        border: 1px solid var(--border); 
                        border-radius: var(--radius-lg); 
                        padding: 1.5rem; 
                        margin-bottom: 1.5rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: var(--primary); font-weight: 600;">Current Session</h4>
                <p style="margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; color: var(--text-secondary); background: var(--bg-tertiary); padding: 0.75rem; border-radius: var(--radius); border: 1px solid var(--border-light);">
                    <strong>Intake ID:</strong> {st.session_state.intake_id}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Check Status", key="status_btn", use_container_width=True):
                    with st.spinner("Retrieving intake status..."):
                        status = get_intake_status(st.session_state.intake_id)
                        if status:
                            st.json(status)
            
            with col2:
                if st.button("Finalize Intake", key="finalize_btn", use_container_width=True):
                    with st.spinner("Finalizing intake session..."):
                        finalize_intake(st.session_state.intake_id)
            
            with col3:
                if st.button("Reset Session", key="reset_btn", use_container_width=True):
                    reset_session()
        
        else:
            st.markdown("""
            <div class="empty-state">
                <h3>Ready to Start?</h3>
                <p>Initialize an intake session above to begin uploading and analyzing your content.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <h2>Query AI Insights</h2>
                <p>Ask questions about your data and get intelligent, contextual insights powered by Pulse</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Query input
        query_text = st.text_area(
            "Ask a question about your data",
            placeholder="Ask questions about your uploaded content...",
            height=150,
            help="Ask specific questions about your uploaded content to get AI-powered insights"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            query_btn = st.button("Get AI Insights", key="query_btn", disabled=not query_text.strip(), use_container_width=True)
        
        with col2:
            if hasattr(st.session_state, 'last_query_response'):
                if st.button("Clear Results", key="clear_results", use_container_width=True):
                    if hasattr(st.session_state, 'last_query_response'):
                        delattr(st.session_state, 'last_query_response')
                    if hasattr(st.session_state, 'last_query'):
                        delattr(st.session_state, 'last_query')
                    st.rerun()
        
        if query_btn:
            with st.spinner("Analyzing..."):
                response = query_insights(query_text)
                if response:
                    st.session_state.last_query_response = response
                    st.session_state.last_query = query_text
        
        # Display response
        if hasattr(st.session_state, 'last_query_response') and st.session_state.last_query_response:
            st.markdown("---")
            st.markdown("### Response")
            
            # Show the question in a clean format
            st.markdown(f"**Question:** {st.session_state.get('last_query', 'Previous query')}")
            st.markdown("")
            
            # Display the response content
            response = st.session_state.last_query_response
            if isinstance(response, dict):
                if 'answer' in response:
                    st.markdown(response['answer'])
                elif 'insights' in response:
                    st.markdown(response['insights'])
                elif 'response' in response:
                    st.markdown(response['response'])
                else:
                    # Format JSON response nicely
                    st.markdown("**Response Data:**")
                    st.json(response)
            else:
                st.markdown(str(response))

    # Meeting Assistant Tab
    with tab3:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <h2>Meeting Assistant</h2>
                <p>Add Scooby AI to your meetings</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Meeting link input section
        st.markdown("#### Meeting Details")
        st.write("Enter your meeting link below to add Scooby to your meeting.")
        
        meeting_link = st.text_input(
            "Meeting Link",
            placeholder="https://meet.google.com/xyz-abcd-123 or https://zoom.us/j/1234567890",
            help="Enter the full meeting URL (Google Meet, Zoom, Microsoft Teams, etc.)",
            key="meeting_link_input"
        )
        
        # Display meeting link info if provided
        if meeting_link.strip():
            st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Detect meeting platform
                platform = "Unknown"
                if "meet.google.com" in meeting_link.lower():
                    platform = "Google Meet"
                elif "zoom.us" in meeting_link.lower():
                    platform = "Zoom"
                elif "teams.microsoft.com" in meeting_link.lower():
                    platform = "Microsoft Teams" 
                elif "webex" in meeting_link.lower():
                    platform = "Webex"
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="font-size: 1rem;">{platform}</div>
                    <div class="metric-label">Platform</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Meeting link validation
                is_valid = any(domain in meeting_link.lower() for domain in ['meet.google.com', 'zoom.us', 'teams.microsoft.com', 'webex'])
                status_text = "Valid" if is_valid else "Check Link"
                
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="font-size: 1rem;">{status_text}</div>
                    <div class="metric-label">Status</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Link length indicator
                link_length = len(meeting_link)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{link_length}</div>
                    <div class="metric-label">Characters</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Meeting link preview
            st.markdown(f"""
            <div style="background: var(--bg-tertiary); border: 1px solid var(--border); border-radius: var(--radius); 
                        padding: 1rem; margin: 1rem 0; font-family: 'JetBrains Mono', monospace; 
                        font-size: 0.875rem; word-break: break-all; color: var(--text-secondary);">
                <strong>Meeting Link:</strong><br>{meeting_link}
            </div>
            """, unsafe_allow_html=True)
            
            # Add Scooby button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Add Scooby to Meeting", key="add_scooby_btn", use_container_width=True, disabled=not meeting_link.strip()):
                    with st.spinner("Adding Scooby to your meeting..."):
                        add_scooby_to_meeting(meeting_link)

def main():
    """Main function to route between login and app"""
    # Track session start time
    if "session_start" not in st.session_state:
        st.session_state.session_start = time.time()
    
    # Initialize authentication state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    # Route to appropriate page
    if st.session_state.authenticated:
        main_app()
    else:
        login_page()

if __name__ == "__main__":
    main()
