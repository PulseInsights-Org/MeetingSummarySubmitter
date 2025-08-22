import streamlit as st
import requests
import uuid
import time
import json
from typing import Optional
from supabase import create_client, Client

# Configuration
API_BASE_URL = "https://dev.pulse-api.getpulseinsights.ai"

# Supabase Configuration
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "your-supabase-url")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY", "your-supabase-anon-key")

@st.cache_resource
def init_supabase() -> Client:
    """Initialize Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def load_modern_css():
    """Load modern CSS with premium design"""
    st.markdown("""
    <style>
    /* Import premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Modern Color System */
    :root {
        /* Primary brand colors */
        --primary-50: #eff6ff;
        --primary-100: #dbeafe;
        --primary-200: #bfdbfe;
        --primary-300: #93c5fd;
        --primary-400: #60a5fa;
        --primary-500: #3b82f6;
        --primary-600: #2563eb;
        --primary-700: #1d4ed8;
        --primary-800: #1e40af;
        --primary-900: #1e3a8a;
        
        /* Neutral colors */
        --gray-25: #fcfcfd;
        --gray-50: #f9fafb;
        --gray-100: #f2f4f7;
        --gray-200: #eaecf0;
        --gray-300: #d0d5dd;
        --gray-400: #98a2b3;
        --gray-500: #667085;
        --gray-600: #475467;
        --gray-700: #344054;
        --gray-800: #1d2939;
        --gray-900: #101828;
        
        /* Semantic colors */
        --success-50: #ecfdf3;
        --success-500: #12b76a;
        --success-600: #039855;
        
        --error-50: #fef3f2;
        --error-500: #f04438;
        --error-600: #d92d20;
        
        --warning-50: #fffaeb;
        --warning-500: #f79009;
        --warning-600: #dc6803;
        
        /* Shadows */
        --shadow-xs: 0 1px 2px 0 rgba(16, 24, 40, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(16, 24, 40, 0.1), 0 1px 2px 0 rgba(16, 24, 40, 0.06);
        --shadow-md: 0 4px 8px -2px rgba(16, 24, 40, 0.1), 0 2px 4px -2px rgba(16, 24, 40, 0.06);
        --shadow-lg: 0 12px 16px -4px rgba(16, 24, 40, 0.08), 0 4px 6px -2px rgba(16, 24, 40, 0.03);
        --shadow-xl: 0 20px 24px -4px rgba(16, 24, 40, 0.08), 0 8px 8px -4px rgba(16, 24, 40, 0.03);
        --shadow-2xl: 0 24px 48px -12px rgba(16, 24, 40, 0.18);
        
        /* Border radius */
        --radius-xs: 2px;
        --radius-sm: 4px;
        --radius-md: 6px;
        --radius-lg: 8px;
        --radius-xl: 12px;
        --radius-2xl: 16px;
        --radius-3xl: 20px;
        --radius-full: 9999px;
        
        /* Spacing */
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 12px;
        --spacing-lg: 16px;
        --spacing-xl: 20px;
        --spacing-2xl: 24px;
        --spacing-3xl: 32px;
        --spacing-4xl: 48px;
        --spacing-5xl: 64px;
    }
    
    /* Reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--gray-25);
        color: var(--gray-900);
        line-height: 1.5;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none !important; }
    .stToolbar { display: none !important; }
    
    /* Login Page Redesign */
    .login-page {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-xl);
        position: relative;
        overflow: hidden;
    }
    
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-3xl);
        padding: var(--spacing-2xl);
        max-width: 480px;
        width: 100%;
        box-shadow: var(--shadow-2xl);
        position: relative;
        z-index: 10;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: var(--spacing-4xl);
    }
    
    .brand-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
        border-radius: var(--radius-2xl);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto var(--spacing-xl);
        font-size: 2rem;
        color: white;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-600), var(--primary-800));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--spacing-sm);
        letter-spacing: -0.02em;
    }
    
    .login-subtitle {
        color: var(--gray-600);
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Form Styles */
    .stTextInput > div > div > input {
        background: var(--gray-25);
        border: 2px solid var(--gray-200);
        border-radius: var(--radius-xl);
        padding: var(--spacing-lg) var(--spacing-xl);
        font-size: 1rem;
        font-weight: 500;
        color: var(--gray-900);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-xs);
        width: 100%;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-500);
        box-shadow: 0 0 0 4px var(--primary-100), var(--shadow-sm);
        outline: none;
        background: white;
    }
    
    /* Modern Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
        color: white;
        border: none;
        border-radius: var(--radius-xl);
        padding: var(--spacing-lg) var(--spacing-2xl);
        font-size: 1rem;
        font-weight: 600;
        font-family: inherit;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
        width: 100%;
        height: 48px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-700), var(--primary-800));
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    /* App Header Redesign */
    .app-header {
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-800) 100%);
        padding: var(--spacing-4xl) var(--spacing-3xl);
        margin: -1rem -2rem var(--spacing-3xl) -2rem;
        border-radius: 0 0 var(--radius-3xl) var(--radius-3xl);
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    
    .app-header-content {
        position: relative;
        z-index: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
    }
    
    .brand-section {
        display: flex;
        align-items: center;
        gap: var(--spacing-xl);
    }
    
    .brand-icon {
        width: 56px;
        height: 56px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-2xl);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: var(--shadow-md);
    }
    
    .brand-text h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .brand-text p {
        font-size: 1.125rem;
        font-weight: 400;
        margin: var(--spacing-xs) 0 0 0;
        opacity: 0.9;
    }
    
    .user-section {
        display: flex;
        align-items: center;
        gap: var(--spacing-lg);
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-2xl);
        padding: var(--spacing-lg) var(--spacing-xl);
        box-shadow: var(--shadow-md);
    }
    
    .user-avatar {
        width: 48px;
        height: 48px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-full);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.25rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .user-info h4 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .user-info p {
        margin: 0;
        font-size: 0.875rem;
        opacity: 0.8;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Modern Card Design */
    .modern-card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-2xl);
        padding: var(--spacing-4xl);
        margin-bottom: var(--spacing-3xl);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-500), var(--primary-600));
        border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: var(--spacing-xl);
        margin-bottom: var(--spacing-3xl);
        padding-bottom: var(--spacing-2xl);
        border-bottom: 1px solid var(--gray-100);
    }
    
    .card-icon {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, var(--primary-500), var(--primary-600));
        border-radius: var(--radius-2xl);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        box-shadow: var(--shadow-md);
    }
    
    .card-content h2 {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--gray-900);
        margin: 0 0 var(--spacing-sm) 0;
        letter-spacing: -0.01em;
    }
    
    .card-content p {
        font-size: 1rem;
        color: var(--gray-600);
        margin: 0;
        line-height: 1.6;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--spacing-sm);
        background: linear-gradient(135deg, var(--success-500), var(--success-600));
        color: white;
        padding: var(--spacing-md) var(--spacing-xl);
        border-radius: var(--radius-full);
        font-size: 0.875rem;
        font-weight: 600;
        box-shadow: var(--shadow-sm);
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: var(--radius-full);
    }
    
    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: var(--spacing-xl);
        margin: var(--spacing-3xl) 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--gray-25) 0%, white 100%);
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-2xl);
        padding: var(--spacing-3xl);
        text-align: center;
        box-shadow: var(--shadow-xs);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--primary-400), var(--primary-600));
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--gray-600);
        margin-top: var(--spacing-md);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Query Response */
    .query-response {
        background: linear-gradient(135deg, var(--primary-25) 0%, var(--primary-50) 100%);
        border: 1px solid var(--primary-200);
        border-radius: var(--radius-2xl);
        padding: var(--spacing-4xl);
        margin-top: var(--spacing-3xl);
        position: relative;
        box-shadow: var(--shadow-sm);
    }
    
    .response-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--primary-800);
        margin: 0 0 var(--spacing-xl) 0;
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
    }
    
    .query-preview {
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid var(--primary-200);
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-xl);
        font-size: 0.9rem;
        color: var(--gray-700);
        font-style: italic;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .login-container { padding: var(--spacing-3xl); }
        .app-header { padding: var(--spacing-3xl) var(--spacing-xl); margin: -1rem -1rem var(--spacing-xl) -1rem; }
        .brand-text h1 { font-size: 2rem; }
        .modern-card { padding: var(--spacing-3xl); }
        .app-header-content { flex-direction: column; gap: var(--spacing-xl); text-align: center; }
        .user-section { flex-direction: column; text-align: center; }
        .card-header { flex-direction: column; text-align: center; }
        .metric-grid { grid-template-columns: 1fr; }
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
            st.error("🚫 Organization not found")
            return False, None
        
        org_data = response.data[0]
        
        if org_data["password"] == password:
            return True, org_data["id"]
        else:
            st.error("🔑 Invalid password")
            return False, None
            
    except Exception as e:
        st.error(f"❌ Authentication error: {str(e)}")
        return False, None

def login_page():
    """Display the modern login page"""
    st.set_page_config(
        page_title="Pulse Copilot - Sign In",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    load_modern_css()
    
    # Full-screen login layout
    st.markdown("""
    <div class="login-page">
        <div class="login-container">
            <div class="login-header">
                <div class="brand-logo">🤖</div>
                <h1 class="login-title">Pulse Copilot</h1>
                <p class="login-subtitle">Sign in to access your AI-powered insights platform</p>
            </div>
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
        
        # Center the submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🔐 Sign In", use_container_width=True)
        
        if submitted:
            if not org_name or not password:
                st.error("⚠️ Please enter both organization name and password")
            else:
                with st.spinner("🔐 Authenticating..."):
                    is_authenticated, org_id = authenticate_user(org_name, password)
                    if is_authenticated:
                        st.session_state.authenticated = True
                        st.session_state.org_name = org_name
                        st.session_state.org_id = org_id
                        st.session_state.password = password
                        st.success("✅ Login successful! Redirecting...")
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
            st.error(f"❌ Failed to initialize intake: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Error initializing intake: {str(e)}")
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
            st.success("✅ File uploaded successfully!")
            st.session_state.idempotency_key = generate_idempotency_key()
            return True
        else:
            st.error(f"❌ Failed to upload file: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"❌ Error uploading file: {str(e)}")
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
            st.success("✅ Text uploaded successfully!")
            st.session_state.idempotency_key = generate_idempotency_key()
            return True
        else:
            st.error(f"❌ Failed to upload text: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"❌ Error uploading text: {str(e)}")
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
            st.error(f"❌ Failed to get intake status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Error getting intake status: {str(e)}")
        return None

def query_insights(query: str) -> Optional[dict]:
    """Query insights from the copilot"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "Authorization": f"Bearer {st.session_state.password}",
            "Content-Type": "application/json"
        }
        
        data = {"query": query}
        
        response = requests.post(f"{API_BASE_URL}/api/copilot/query", headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Failed to query insights: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Error querying insights: {str(e)}")
        return None

def finalize_intake(intake_id: str) -> bool:
    """Finalize the intake"""
    try:
        headers = {
            "x-org-id": str(st.session_state.org_id),
            "Authorization": f"Bearer {st.session_state.password}"
        }
        
        response = requests.post(f"{API_BASE_URL}/api/intakes/{intake_id}/finalize", headers=headers)
        
        if response.status_code == 200:
            st.success("✅ Intake finalized successfully!")
            return True
        else:
            st.error(f"❌ Failed to finalize intake: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"❌ Error finalizing intake: {str(e)}")
        return False

def reset_session():
    """Reset the session and clear all state"""
    st.session_state.intake_id = None
    st.session_state.intake_initialized = False
    st.session_state.idempotency_key = None
    if hasattr(st.session_state, 'last_query_response'):
        delattr(st.session_state, 'last_query_response')
    st.success("🔄 Session reset successfully!")
    st.rerun()

def logout():
    """Logout and clear authentication"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("👋 Logged out successfully!")
    time.sleep(1)
    st.rerun()

def main_app():
    """Main application with modern design"""
    st.set_page_config(
        page_title="Pulse Copilot - Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    load_modern_css()
    
    # Modern Header
    org_initial = st.session_state.org_name[0].upper() if st.session_state.org_name else "O"
    
    st.markdown(f"""
    <div class="app-header">
        <div class="app-header-content">
            <div class="brand-section">
                <div class="brand-icon">🤖</div>
                <div class="brand-text">
                    <h1>Pulse Copilot</h1>
                    <p>AI-powered insights for your organization</p>
                </div>
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
    
    # Logout button prominently displayed
    col1, col2, col3 = st.columns([6, 1, 2])
    with col3:
        if st.button("👋 Sign Out", key="logout_btn", use_container_width=True):
            logout()
    
    # Add some spacing after logout button
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize session state
    if "intake_id" not in st.session_state:
        st.session_state.intake_id = None
    if "intake_initialized" not in st.session_state:
        st.session_state.intake_initialized = False
    if "idempotency_key" not in st.session_state:
        st.session_state.idempotency_key = None
    
    # Modern tabs
    tab1, tab2, tab3 = st.tabs(["📥 Data Intake", "🔍 Query Insights", "⚙️ Management"])
    
    with tab1:
        # Step 1: Initialize Intake
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <div class="card-icon">1</div>
                <div class="card-content">
                    <h2>Initialize Intake Session</h2>
                    <p>Start a new session to upload and analyze your content with AI-powered insights</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Initialize New Intake", key="init_btn", use_container_width=True):
                with st.spinner("🔄 Initializing intake session..."):
                    intake_id = init_intake()
                    if intake_id:
                        st.session_state.intake_id = intake_id
                        st.session_state.intake_initialized = True
                        st.success("✅ Intake session initialized successfully!")
                        st.balloons()
        
        if st.session_state.intake_initialized:
            st.markdown(f"""
            <div style="text-align: center; margin-top: 2rem;">
                <div class="status-badge">
                    <div class="status-indicator"></div>
                    Active Session: {st.session_state.intake_id[:8]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Step 2: Upload Content
        if st.session_state.intake_initialized:
            st.markdown("""
            <div class="modern-card">
                <div class="card-header">
                    <div class="card-icon">2</div>
                    <div class="card-content">
                        <h2>Upload Your Content</h2>
                        <p>Add documents, files, or text content for AI analysis and insights generation</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            upload_tab1, upload_tab2 = st.tabs(["📄 File Upload", "✏️ Text Input"])
            
            with upload_tab1:
                st.markdown("#### 📎 Upload Documents")
                st.write("Upload files containing your meeting notes, reports, research, or any text content.")
                
                uploaded_file = st.file_uploader(
                    "Choose a file",
                    type=["txt", "md", "pdf", "docx"],
                    help="Supported formats: .txt, .md, .pdf, .docx (Max 10MB)",
                    label_visibility="collapsed"
                )
                
                if uploaded_file is not None:
                    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">File Name</div>
                            <div style="font-weight: 600; color: var(--gray-900); font-size: 0.9rem; margin-top: 0.5rem; word-break: break-all;">
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
                        if st.button("📤 Upload File", key="upload_file_btn", use_container_width=True):
                            with st.spinner("📤 Uploading and processing your file..."):
                                if upload_file(st.session_state.intake_id, uploaded_file):
                                    st.balloons()
            
            with upload_tab2:
                st.markdown("#### ✏️ Direct Text Input")
                st.write("Enter your content directly for immediate analysis and processing.")
                
                text_content = st.text_area(
                    "Content",
                    placeholder="Paste your meeting notes, research findings, reports, or any text content here...\n\nExample:\n- Meeting summary from Q4 planning session\n- Customer feedback analysis\n- Project status reports\n- Research findings",
                    height=300,
                    help="Enter any text content you'd like to analyze",
                    label_visibility="collapsed"
                )
                
                if text_content.strip():
                    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
                    
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
                        if st.button("📝 Upload Text", key="upload_text_btn", use_container_width=True):
                            with st.spinner("📝 Processing and analyzing your text..."):
                                if upload_text(st.session_state.intake_id, text_content):
                                    st.balloons()
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="modern-card">
                <div style="text-align: center; padding: 2rem 0;">
                    <h3 style="color: var(--gray-600); margin-bottom: 1rem;">📥 Ready to Start?</h3>
                    <p style="color: var(--gray-500); margin-bottom: 2rem;">Initialize an intake session above to begin uploading and analyzing your content.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <div class="card-icon">🔍</div>
                <div class="card-content">
                    <h2>Query AI Insights</h2>
                    <p>Ask questions about your data and get intelligent, contextual insights powered by AI</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Query input with better UX
        query_text = st.text_area(
            "Ask a question about your data",
            placeholder="Ask questions about your uploaded content to get AI-powered insights...\n\nExample questions:\n- What are the key findings from the uploaded documents?\n- Summarize the main points from our meeting notes\n- What action items were identified?\n- What are the biggest risks mentioned?",
            height=150,
            help="Ask specific questions about your uploaded content to get AI-powered insights"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            query_btn = st.button("🔍 Get AI Insights", key="query_btn", disabled=not query_text.strip(), use_container_width=True)
        
        with col2:
            if hasattr(st.session_state, 'last_query_response'):
                if st.button("🗑️ Clear Results", key="clear_results", use_container_width=True):
                    if hasattr(st.session_state, 'last_query_response'):
                        delattr(st.session_state, 'last_query_response')
                    if hasattr(st.session_state, 'last_query'):
                        delattr(st.session_state, 'last_query')
                    st.rerun()
        
        if query_btn:
            with st.spinner("🤖 AI is analyzing your data and generating insights..."):
                response = query_insights(query_text)
                if response:
                    st.session_state.last_query_response = response
                    st.session_state.last_query = query_text
        
        # Display response with modern styling
        if hasattr(st.session_state, 'last_query_response') and st.session_state.last_query_response:
            st.markdown(f"""
            <div class="query-response">
                <h3 class="response-header">🤖 AI Insights</h3>
                <div class="query-preview">
                    <strong>Your Question:</strong> {st.session_state.get('last_query', 'Previous query')}
                </div>
            """, unsafe_allow_html=True)
            
            response = st.session_state.last_query_response
            if isinstance(response, dict):
                if 'answer' in response:
                    st.markdown(response['answer'])
                elif 'insights' in response:
                    st.markdown(response['insights'])
                elif 'response' in response:
                    st.markdown(response['response'])
                else:
                    st.json(response)
            else:
                st.markdown(str(response))
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="modern-card">
            <div class="card-header">
                <div class="card-icon">⚙️</div>
                <div class="card-content">
                    <h2>Session Management</h2>
                    <p>Manage your current intake session, view statistics, and system information</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.intake_initialized:
            # Current session info
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, var(--primary-25) 0%, var(--primary-50) 100%); 
                        border: 1px solid var(--primary-200); 
                        border-radius: var(--radius-2xl); 
                        padding: var(--spacing-3xl); 
                        margin-bottom: var(--spacing-3xl);
                        position: relative;">
                <h4 style="margin: 0 0 var(--spacing-md) 0; color: var(--primary-800); font-weight: 700;">🎯 Current Session</h4>
                <p style="margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: var(--gray-700); background: rgba(255,255,255,0.7); padding: var(--spacing-md); border-radius: var(--radius-lg);">
                    <strong>Intake ID:</strong> {st.session_state.intake_id}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Check Status", key="status_btn", use_container_width=True):
                    with st.spinner("📊 Retrieving intake status..."):
                        status = get_intake_status(st.session_state.intake_id)
                        if status:
                            st.json(status)
            
            with col2:
                if st.button("✅ Finalize Intake", key="finalize_btn", use_container_width=True):
                    with st.spinner("✅ Finalizing intake session..."):
                        if finalize_intake(st.session_state.intake_id):
                            st.balloons()
            
            with col3:
                if st.button("🔄 Reset Session", key="reset_btn", use_container_width=True):
                    reset_session()
            
            # Session Statistics
            st.markdown("#### 📈 Session Statistics")
            
            st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">1</div>
                    <div class="metric-label">Active Session</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                upload_count = len([k for k in st.session_state.keys() if 'upload' in k.lower()])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{upload_count}</div>
                    <div class="metric-label">Uploads</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                query_count = 1 if hasattr(st.session_state, 'last_query_response') else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{query_count}</div>
                    <div class="metric-label">AI Queries</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                session_time = time.time() - st.session_state.get('session_start', time.time())
                minutes = int(session_time // 60)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{minutes}</div>
                    <div class="metric-label">Minutes Active</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: var(--spacing-4xl) 0; background: var(--gray-25); border-radius: var(--radius-2xl); border: 1px solid var(--gray-200);">
                <h3 style="color: var(--gray-600); margin-bottom: var(--spacing-lg);">🎯 No Active Session</h3>
                <p style="color: var(--gray-500); margin-bottom: var(--spacing-2xl);">Initialize an intake session in the 'Data Intake' tab to access management features.</p>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Go to Data Intake", key="goto_intake", use_container_width=True):
                    st.info("Switch to the 'Data Intake' tab above to initialize a session.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # System Information
        with st.expander("ℹ️ System Information", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **🏢 Organization:** {st.session_state.org_name}  
                **🆔 Organization ID:** `{st.session_state.org_id}`  
                **⏰ Session Started:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
                **🌐 Location:** Bengaluru, Karnataka, IN
                """)
            
            with col2:
                st.markdown(f"""
                **🔗 API Endpoint:** `{API_BASE_URL}`  
                **📊 Streamlit Version:** `{st.__version__}`  
                **🔐 Authentication:** Active ✅  
                **💻 Platform:** Streamlit Cloud
                """)

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
