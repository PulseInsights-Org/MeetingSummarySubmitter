import streamlit as st
import requests
import uuid
import time
import json
from typing import Optional

# Configuration
API_BASE_URL = "https://dev.pulse-api.getpulseinsights.ai"
ORG_ID = "pulse-dev"

def generate_idempotency_key():
    """Generate a unique idempotency key"""
    return str(uuid.uuid4())

def init_intake() -> Optional[str]:
    """Initialize a new intake and return the intake_id"""
    try:
        headers = {
            "x-org-id": ORG_ID,
            "x-idempotency-key": generate_idempotency_key()
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/intakes/init",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("intake_id")
        else:
            st.error(f"Failed to initialize intake: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error initializing intake: {str(e)}")
        return None

def upload_file(intake_id: str, uploaded_file) -> bool:
    """Upload a file to the intake"""
    try:
        headers = {
            "x-org-id": ORG_ID
        }
        
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/upload/file/{intake_id}",
            headers=headers,
            files=files
        )
        
        if response.status_code == 200:
            st.success("File uploaded successfully!")
            return True
        else:
            st.error(f"Failed to upload file: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return False

def upload_text(intake_id: str, text_content: str) -> bool:
    """Upload text content to the intake"""
    try:
        headers = {
            "x-org-id": ORG_ID
        }
        
        data = {
            "text_content": text_content
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/upload/text/{intake_id}",
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            st.success("Text uploaded successfully!")
            return True
        else:
            st.error(f"Failed to upload text: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error uploading text: {str(e)}")
        return False

def get_intake_status(intake_id: str) -> Optional[dict]:
    """Get the status of an intake"""
    try:
        headers = {
            "x-org-id": ORG_ID
        }
        
        response = requests.get(
            f"{API_BASE_URL}/api/intakes/{intake_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get intake status: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error getting intake status: {str(e)}")
        return None

def finalize_intake(intake_id: str) -> bool:
    """Finalize the intake"""
    try:
        headers = {
            "x-org-id": ORG_ID
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/intakes/{intake_id}/finalize",
            headers=headers
        )
        
        if response.status_code == 200:
            st.success("Intake finalized successfully!")
            return True
        else:
            st.error(f"Failed to finalize intake: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error finalizing intake: {str(e)}")
        return False

def main():
    st.set_page_config(
        page_title="Pulse API Client",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("Pulse API Client")
    st.markdown("---")
    
    # Initialize session state
    if "intake_id" not in st.session_state:
        st.session_state.intake_id = None
    if "intake_initialized" not in st.session_state:
        st.session_state.intake_initialized = False
    
    # Step 1: Initialize Intake
    st.header("Step 1: Initialize Intake")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("Initialize New Intake", type="secondary"):
            with st.spinner("Initializing intake..."):
                intake_id = init_intake()
                if intake_id:
                    st.session_state.intake_id = intake_id
                    st.session_state.intake_initialized = True
                    st.success(f"Intake initialized with ID: `{intake_id}`")
    
    
    # Only show upload options if intake is initialized
    if st.session_state.intake_initialized:
        st.markdown("---")
        
        # Step 2: Upload Content
        st.header("Step 2: Upload Content")
        
        # Create tabs for file upload and text input
        tab1, tab2 = st.tabs(["📁 File Upload", "📝 Text Input"])
        
        with tab1:
            st.subheader("Upload File (.txt or .md)")
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=["txt", "md"],
                help="Upload a .txt or .md file containing your content"
            )
            
            if uploaded_file is not None:
                st.write("**File Details:**")
                st.write(f"- Name: {uploaded_file.name}")
                st.write(f"- Type: {uploaded_file.type}")
                st.write(f"- Size: {uploaded_file.size} bytes")
                
                if st.button("📤 Upload File", key="upload_file_btn"):
                    with st.spinner("Uploading file..."):
                        upload_file(st.session_state.intake_id, uploaded_file)
        
        with tab2:
            st.subheader("Upload Text Content")
            text_content = st.text_area(
                "Enter your text content:",
                placeholder="Enter your meeting notes, summary, or any text content here...",
                height=200
            )
            
            if text_content.strip():
                st.write(f"**Character count:** {len(text_content)}")
                
                if st.button("📤 Upload Text", key="upload_text_btn"):
                    with st.spinner("Uploading text..."):
                        upload_text(st.session_state.intake_id, text_content)
        
        st.markdown("---")
        
        # Step 3: Management Actions
        st.header("Step 3: Management Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Check Status", type="secondary"):
                with st.spinner("Getting intake status..."):
                    status = get_intake_status(st.session_state.intake_id)
                    if status:
                        st.json(status)
        
        with col2:
            if st.button("✅ Finalize Intake", type="secondary"):
                with st.spinner("Finalizing intake..."):
                    finalize_intake(st.session_state.intake_id)
        
        with col3:
            if st.button("🔄 Reset Session", type="secondary"):
                st.session_state.intake_id = None
                st.session_state.intake_initialized = False
                st.rerun()
    
  
if __name__ == "__main__":
    main()
