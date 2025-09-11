import streamlit as st
import uuid
import os
from agents_upd import build_agent
import time
import networkx as nx
import matplotlib.pyplot as plt

# Output folder for generated code
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def visualize_langgraph(agent):
    G = nx.DiGraph()

    graph = agent.get_graph()  # Get internal graph

    # Add nodes
    for node in graph.nodes:
        G.add_node(node)

    # Add edges
    for edge in graph.edges:
        # Defensive unpacking: take first two elements as src, dest
        src, dest = edge[0], edge[1]

        if str(dest).upper() == "END":
            G.add_node("END")
            G.add_edge(src, "END")
        else:
            G.add_edge(src, dest)

    # Draw graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2500, arrowsize=20)
    plt.title("LangGraph Workflow Visualization")
    st.pyplot(plt)
    plt.close()



def save_code_to_file(code: str) -> str:
    filename = f"springboot_microservice_{uuid.uuid4()}.java"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    return filepath


def main():
    # Use wide layout to utilize full screen width
    st.set_page_config(
        page_title="Legacy Java to Spring Boot Converter",
        layout="wide",
        page_icon="🧠",
    )

    st.markdown("<h1 style='text-align: center;'>🧠 Legacy Java → 🚀 Spring Boot Microservice</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Powered by LangGraph Agentic AI</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Upload section
    st.markdown("### 📦 Upload Legacy Java Codebase")
    uploaded_file = st.file_uploader("Upload your legacy Java codebase (.zip)", type=["zip"])

    if uploaded_file:
        zip_path = os.path.join(OUTPUT_DIR, f"upload_{uuid.uuid4()}.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.success("✅ File uploaded successfully!")
        st.markdown("---")

        # Process and simulate progress
        with st.spinner("🚀 Running LangGraph agent on your code..."):
            agent = build_agent()
            print(dir(agent))
            print([m for m in dir(agent) if 'dot' in m or 'graph' in m or 'visual' in m])

            st.info("🔍 Parsing the uploaded Java code...")
            time.sleep(1)

            result_state = agent.invoke({"zip_path": zip_path})

            st.info("📄 Generating documentation...")
            time.sleep(1)

            st.info("⚙️ Generating Spring Boot code...")
            time.sleep(1)

            code_file = save_code_to_file(result_state["springboot_code"])
            time.sleep(1)
            visualize_langgraph(agent)
        st.success("✅ Code generation complete!")
        st.markdown("---")

        # Tabs to separate Documentation and Code Output
        tabs = st.tabs(["📄 Documentation", "💻 Spring Boot Code"])

        with tabs[0]:
            st.markdown("### 📄 Generated Documentation (Interactive JSON Viewer)")
            st.info("You can expand/collapse nested sections of the JSON.")
            st.json(result_state["documentation"])

        with tabs[1]:
            st.markdown("### 💻 Generated Spring Boot Code")
            st.success("Below is the generated microservice code. You can copy or download it.")

            with st.expander("📂 View Spring Boot Code", expanded=True):
                st.code(result_state["springboot_code"], language="java")

            with open(code_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download Spring Boot Code",
                    data=f,
                    file_name=os.path.basename(code_file),
                    mime="text/plain",
                )

        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: gray;'>✨ Thank you for using the Legacy → Spring Boot Generator ✨</p>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
