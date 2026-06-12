import streamlit as st
import database
import pandas as pd

def render():
    st.header("🛡️ User Management")
    st.markdown("Manage system access, roles, and account statuses.")
    
    # 1. View Users
    st.subheader("Current Users")
    users_df = database.get_all_users()
    if not users_df.empty:
        # Map acc_sts for display
        users_df['Status'] = users_df['acc_sts'].apply(lambda x: 'Active' if x == 1 else 'Inactive')
        display_df = users_df[['id', 'username', 'role', 'Status']]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No users found.")
        
    st.divider()
    
    col1, col2 = st.columns(2)
    
    # 2. Add New User
    with col1:
        st.subheader("Add New User")
        with st.form("add_user_form", clear_on_submit=True):
            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["USER", "ADMIN"])
            new_sts = st.selectbox("Status", ["Active", "Inactive"])
            
            submit_add = st.form_submit_button("Create User", use_container_width=True)
            if submit_add:
                if new_user and new_pass:
                    sts_int = 1 if new_sts == "Active" else 0
                    if database.add_user(new_user, new_pass, new_role, sts_int):
                        st.success(f"User '{new_user}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to create user. Username might already exist.")
                else:
                    st.warning("Please fill in both username and password.")
                    
    # 3. Update Existing User
    with col2:
        st.subheader("Update Existing User")
        if not users_df.empty:
            with st.form("update_user_form"):
                user_to_update = st.selectbox("Select User to Update", users_df['username'].tolist())
                # Get current details to prefill
                current_data = users_df[users_df['username'] == user_to_update].iloc[0]
                upd_role = st.selectbox("New Role", ["USER", "ADMIN"], index=0 if current_data['role'] == 'USER' else 1)
                upd_sts = st.selectbox("New Status", ["Active", "Inactive"], index=0 if current_data['acc_sts'] == 1 else 1)
                
                submit_upd = st.form_submit_button("Update Status/Role", use_container_width=True)
                
                if submit_upd:
                    if user_to_update == 'admin' and upd_sts == 'Inactive':
                        st.error("Cannot deactivate the primary admin account!")
                    else:
                        sts_int = 1 if upd_sts == "Active" else 0
                        if database.update_user_status(int(current_data['id']), upd_role, sts_int):
                            st.success(f"User '{user_to_update}' updated successfully!")
                            st.rerun()
                        else:
                            st.error("Update failed.")
                            
            with st.form("reset_pass_form", clear_on_submit=True):
                st.markdown("**Reset Password**")
                user_to_reset = st.selectbox("Select User", users_df['username'].tolist(), key="reset_user_sel")
                reset_pass = st.text_input("New Password", type="password")
                submit_reset = st.form_submit_button("Reset Password", use_container_width=True)
                
                if submit_reset:
                    if reset_pass:
                        user_id = int(users_df[users_df['username'] == user_to_reset].iloc[0]['id'])
                        if database.reset_user_password(user_id, reset_pass):
                            st.success(f"Password for '{user_to_reset}' reset successfully!")
                        else:
                            st.error("Failed to reset password.")
                    else:
                        st.warning("Please enter a new password.")
        else:
            st.info("No users to update.")
