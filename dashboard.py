import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import requests
import time
import random
import pandas as pd

st.set_page_config(page_title="Quantum Hub", layout="wide")
st.title("🛡️ Quantum Mesh: Self-Healing Dashboard")

# Professional White Background Styling
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white"
})


def run_dashboard():
    try:
        response = requests.get("http://127.0.0.1:5000/get_state")
        state = response.json()
    except:
        st.error("System Sync Error: Server not responding.")
        return

    noise_map = state.get("noise_map", {})
    current_route = state.get("active_route", ["London", "Paris", "Berlin", "Vienna"])
    bob_data = state.get("bob_results", {})
    eff = bob_data.get("efficiency", 0.0)
    sifting_log = bob_data.get("sifting_log", [])

    cities = ["London", "Paris", "Berlin", "Brussels", "Amsterdam",
              "Munich", "Prague", "Vienna", "Madrid", "Lyon"]

    G = nx.Graph()

    # 1. Build Graph with Infinite Penalties for Noisy Links
    for i, u in enumerate(cities):
        for v in cities[i + 1:]:
            k1, k2 = f"{u}-{v}", f"{v}-{u}"
            val = noise_map.get(k1, noise_map.get(k2, 0.1))

            # Mathematical forcing: if noise > 0.4, link is effectively infinite
            weight = 1000000.0 if val > 0.4 else (1.0 + val)
            G.add_edge(u, v, weight=weight)

    # 2. Autonomous Reroute Logic
    try:
        new_path = nx.shortest_path(G, source="London", target="Vienna", weight='weight')
        if new_path != current_route:
            requests.post("http://127.0.0.1:5000/update_route", json={"route": new_path})
            current_route = new_path
    except:
        st.error("Operational Alert: Target unreachable through secure paths.")

    # 3. Network Map Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.circular_layout(G)
    nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color='black', ax=ax)

    # Active Path (Green)
    path_edges = list(zip(current_route, current_route[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=5, ax=ax)

    # Noise Indicators (Red Dashed)
    for link, val in noise_map.items():
        if val > 0.4:
            try:
                u_n, v_n = link.split('-')
                nx.draw_networkx_edges(G, pos, edgelist=[(u_n, v_n)], edge_color='red', width=2, style='dashed', ax=ax)
            except:
                pass

    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='#F0F2F6', edgecolors='black', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif', ax=ax)
    ax.axis('off')
    st.pyplot(fig)

    # 4. Key Sifting Table and Shared Secret
    st.divider()
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.subheader("Quantum Key Sifting (BB84)")
        if sifting_log:
            df = pd.DataFrame(sifting_log)

            def highlight_status(val):
                color = 'green' if 'KEPT' in val else 'red' if 'ERROR' in val else 'gray'
                return f'color: {color}'

            st.table(df.style.applymap(highlight_status, subset=['Status']))
        else:
            st.info("Awaiting initial quantum transmission...")

    with col_b:
        st.subheader("Final Secret Key")
        secret_key = "".join(
            [str(item['Resulting Key Bit']) for item in sifting_log if item['Status'] == "KEPT (Success)"])
        if secret_key:
            st.success(f"**Shared Key:** `{secret_key}`")
        else:
            st.warning("Insufficient successful bits for key generation.")

        st.write(f"**Efficiency:** {eff:.1%}")
        st.write(f"**Current Path:** {' ➔ '.join(current_route)}")


if __name__ == "__main__":
    run_dashboard()
    time.sleep(1)
    st.rerun()