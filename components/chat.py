import time
import streamlit as st
import config
import prompts
import utils

def render_chat_workspace(ai_client):
    """
    Renders the interactive chat workspace.
    Handles messages, inputs, streaming, metrics, copy, downloads, and feedback.
    """
    st.markdown("# 💬 Interactive Chat Workspace")
    st.markdown("Configure your prompt template, select your style, and converse with the model.")
    
    # Workspace Config Area
    config_col1, config_col2, config_col3 = st.columns([2, 1, 1])
    
    with config_col1:
        st.session_state.current_feature = st.selectbox(
            "Select AI Feature / Tool",
            options=list(config.FEATURES.keys()),
            index=list(config.FEATURES.keys()).index(st.session_state.current_feature)
        )
    
    with config_col2:
        st.session_state.prompt_style = st.selectbox(
            "Prompt Style Depth",
            options=["Concise", "Medium", "Detailed"],
            index=["Concise", "Medium", "Detailed"].index(st.session_state.prompt_style)
        )
        
    with config_col3:
        st.write("") # Spacer
        st.write("") # Spacer
        clear_col1, clear_col2 = st.columns(2)
        with clear_col1:
            st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
            if st.button("🧹 Clear", use_container_width=True, help="Clear active conversation history"):
                st.session_state.messages = []
                st.session_state.feedback_submitted = {}
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with clear_col2:
            if st.button("➕ New Chat", use_container_width=True, help="Save active session to History and start fresh"):
                if len(st.session_state.messages) > 0:
                    session_summary = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "feature": st.session_state.current_feature,
                        "messages": st.session_state.messages.copy()
                    }
                    st.session_state.history.append(session_summary)
                st.session_state.messages = []
                st.session_state.feedback_submitted = {}
                st.rerun()

    active_feat = st.session_state.current_feature
    active_style = st.session_state.prompt_style
    st.info(
        f"**Active Feature:** {active_feat} ({config.FEATURES[active_feat]['icon']}) | "
        f"**Prompt Style:** {active_style}\n\n"
        f"*Using system profile template:* \"{prompts.SYSTEM_PROMPTS[active_feat][active_style][:100]}...\""
    )

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Display Chat History
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            # Show parameters & response metrics only for assistant's message
            if msg["role"] == "assistant":
                cols = st.columns([1.5, 1, 1.5, 2])
                with cols[0]:
                    st.caption(f"⏱️ **Time:** {msg.get('response_time', 0.0):.2f}s")
                with cols[1]:
                    st.caption(f"✍️ **Words:** {msg.get('word_count', 0)}")
                with cols[2]:
                    response_text = msg["content"]
                    st.download_button(
                        label="📥 Download TXT",
                        data=response_text,
                        file_name=f"mohith_ai_{active_feat.replace(' ', '_').lower()}_{idx}.txt",
                        mime="text/plain",
                        key=f"download_{idx}"
                    )
                with cols[3]:
                    with st.expander("📋 Copy Code/Raw", expanded=False):
                        st.code(response_text, language="text")

                # Feedback widget
                st.write("---")
                feedback_key = f"fb_status_{idx}"
                
                if idx in st.session_state.feedback_submitted:
                    st.success("Thank you for your feedback! (Recorded in feedback.csv)")
                else:
                    st.write("**Was this response helpful?**")
                    fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 4])
                    
                    with fb_col1:
                        yes_clicked = st.button("👍 Yes", key=f"yes_{idx}")
                    with fb_col2:
                        no_clicked = st.button("👎 No", key=f"no_{idx}")
                        
                    if yes_clicked or no_clicked:
                        st.session_state.feedback_submitted[idx] = {
                            "helpful": "Yes" if yes_clicked else "No",
                            "show_form": True
                        }
                        st.rerun()
                        
                if idx in st.session_state.feedback_submitted and st.session_state.feedback_submitted[idx].get("show_form"):
                    status = st.session_state.feedback_submitted[idx]["helpful"]
                    st.markdown(f"Selected: **{status}**")
                    with st.form(key=f"feedback_form_{idx}"):
                        comment = st.text_area("Optional Comment / Suggestion:", placeholder="Tell us how we can improve...")
                        submit_fb = st.form_submit_button("Submit Feedback")
                        
                        if submit_fb:
                            utils.save_feedback_to_csv(
                                feature=msg.get("feature", active_feat),
                                model=st.session_state.model,
                                prompt_style=msg.get("prompt_style", active_style),
                                prompt_input=msg.get("prompt_input", ""),
                                response=msg["content"],
                                helpful=status,
                                comment=comment
                            )
                            st.session_state.feedback_submitted[idx]["show_form"] = False
                            st.success("Feedback saved successfully!")
                            st.rerun()

    # Chat Input
    placeholder_text = prompts.USER_TEMPLATES[active_feat]["placeholder"]
    user_input = st.chat_input(placeholder_text)
    
    # Regenerate response handler
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "assistant":
        if st.button("🔄 Regenerate Response", key="regenerate_btn"):
            if st.session_state.last_api_request:
                st.session_state.messages.pop()
                user_input = st.session_state.last_api_request["user_input"]
                active_feat = st.session_state.last_api_request["feature"]
                active_style = st.session_state.last_api_request["prompt_style"]

    # Trigger Generation on user input
    if user_input:
        if not user_input.strip():
            st.error("Input query cannot be empty. Please enter some text.")
        elif not st.session_state.api_key:
            st.error("OpenRouter API Key is missing! Please configure it in the 'Settings' tab.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.rerun()
            
    # Process generation if user message is the last message
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        user_message = st.session_state.messages[-1]["content"]
        
        with st.chat_message("assistant"):
            sys_prompt = prompts.SYSTEM_PROMPTS[active_feat][active_style]
            user_prompt = prompts.USER_TEMPLATES[active_feat]["formatter"](user_message)
            
            payload_messages = [
                {"role": "system", "content": sys_prompt}
            ]
            
            for msg in st.session_state.messages[:-1]:
                payload_messages.append({"role": msg["role"], "content": msg["content"]})
                
            payload_messages.append({"role": "user", "content": user_prompt})
            
            start_time = time.time()
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Optimized streaming loop using persistent client wrapper
                stream = ai_client.generate_chat_response_stream(
                    messages=payload_messages,
                    model=st.session_state.model,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens
                )
                
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                response_time = time.time() - start_time
                word_count = utils.calculate_word_count(full_response)
                
                st.session_state.last_api_request = {
                    "user_input": user_message,
                    "feature": active_feat,
                    "prompt_style": active_style
                }
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "response_time": response_time,
                    "word_count": word_count,
                    "feature": active_feat,
                    "prompt_style": active_style,
                    "prompt_input": user_message
                })
                
                st.rerun()
                
            except Exception as e:
                message_placeholder.empty()
                st.error(f"⚠️ API Error: {str(e)}")
                st.session_state.messages.pop()
