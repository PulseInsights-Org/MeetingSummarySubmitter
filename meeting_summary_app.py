import streamlit as st
import requests
import json
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Meeting Summary Submitter",
    page_icon="📝",
    layout="centered"
)

# App title and description
st.title("📝 Meeting Summary Submitter")

# Sidebar for endpoint configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    endpoint_url = st.text_input(
        "API Endpoint URL",
        placeholder="https://your-api.com/meeting-summary",
        help="Enter the endpoint where meeting summaries will be sent"
    )
    
    # Optional headers configuration
    st.subheader("Headers (Optional)")
    use_auth = st.checkbox("Add Authorization Header")
    auth_token = ""
    if use_auth:
        auth_token = st.text_input(
            "Authorization Token",
            type="password",
            placeholder="Bearer your-token-here"
        )
    
    # Content type selection
    content_type = st.selectbox(
        "Content Type",
        ["application/json", "text/plain"],
        index=0
    )

# Main form
with st.container():
    st.subheader("📄 Meeting Summary")
    
    # Meeting details form
    col1, col2 = st.columns(2)
    
   
    
    # Meeting summary text area
    meeting_summary = st.text_area(
        "Meeting Summary",
        placeholder="Enter your meeting summary here...",
        height=300,
        help="Provide a detailed summary of the meeting"
    )
    
   

# Submit button and logic
st.markdown("---")

if st.button("🚀 Submit Meeting Summary", type="primary", use_container_width=True):
    # Validation
    if not meeting_summary.strip():
        st.error("❌ Please enter a meeting summary before submitting.")
    elif not endpoint_url.strip():
        st.error("❌ Please configure the API endpoint URL in the sidebar.")
    else:
        # Prepare the data
        if content_type == "application/json":
            payload = {
                "title": meeting_title,
                "date": meeting_date.isoformat(),
                "summary": meeting_summary,
                "attendees": [name.strip() for name in attendees.split(",") if name.strip()] if attendees else [],
                "action_items": action_items.split("\n") if action_items else [],
                "timestamp": datetime.now().isoformat()
            }
        else:
            # For text/plain, send just the summary
            payload = meeting_summary
        
        # Prepare headers
        headers = {"Content-Type": content_type}
        if use_auth and auth_token:
            headers["Authorization"] = auth_token
        
        # Show spinner while submitting
        with st.spinner("Submitting meeting summary..."):
            try:
                # Make the API request
                if content_type == "application/json":
                    response = requests.post(
                        endpoint_url,
                        json=payload,
                        headers=headers,
                        timeout=30
                    )
                else:
                    response = requests.post(
                        endpoint_url,
                        data=payload,
                        headers=headers,
                        timeout=30
                    )
                
                # Handle response
                if response.status_code == 200 or response.status_code == 201:
                    st.success("✅ Meeting summary submitted successfully!")
                    
                    # Show response details in expandable section
                    with st.expander("📄 Response Details"):
                        st.json({
                            "status_code": response.status_code,
                            "response": response.text if response.text else "No response body"
                        })
                    
                    # Option to clear form
                    if st.button("🔄 Clear Form"):
                        st.experimental_rerun()
                        
                else:
                    st.error(f"❌ Failed to submit meeting summary. Status code: {response.status_code}")
                    with st.expander("🔍 Error Details"):
                        st.text(f"Response: {response.text}")
                        
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Please check your endpoint and try again.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection error. Please check your endpoint URL and internet connection.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Request failed: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
