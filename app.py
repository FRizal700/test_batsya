import streamlit as st
from PIL import Image
from io import BytesIO
import os
import base64

# ========== KONFIGURASI ==========
COMPONENTS = {
    "Mata": {
        "1": "assets/Eyes1.png",
        "2": "assets/Eyes2.png",
        "3": "assets/Eyes3.png",
        "4": "assets/Eyes4.png",
        "5": "assets/Eyes5.png",
        "6": "assets/Eyes6.png",
        "7": "assets/Eyes7.png"
    },
    "Mulut": {
        "m1": "assets/m1.png",
        "m2": "assets/m2.png",
        "m3": "assets/m3.png",
        "m4": "assets/m4.png",
        "m5": "assets/m5.png",
        "m6": "assets/m6.png",
        "m7": "assets/m7.png",
        "m8": "assets/m8.png",
        "m9": "assets/m9.png"
    },
    "Baju": {
        "c0": "assets/c0.png",
        "c1": "assets/c1.png",
        "c2": "assets/c2.png",
        "c3": "assets/c3.png",
        "c4": "assets/c4.png",
        "c5": "assets/c5.png",
        "c6": "assets/c6.png",
        "c7": "assets/c7.png",
        "c8": "assets/c8.png",
        "c9": "assets/c9.png"
    },
    "Aksesoris": {
        "g1": "assets/g1.webp",
        "g2": "assets/g2.webp",
        "g3": "assets/g3.webp",
        "g4": "assets/g4.webp",
        "g5": "assets/g5.webp",
        "None": None
    }
}

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def load_image(path):
    try:
        return Image.open(path).convert("RGBA")
    except:
        st.error(f"File tidak ditemukan: {path}")
        return None

def main():
    st.set_page_config(layout="centered", page_title="🎨Batsya Editor🎨")
    st.title("🦥Batsya Custom🦝")
    
    # Inisialisasi state
    if 'selected' not in st.session_state:
        st.session_state.selected = {
            "Base": "assets/base.png",
            "Mata": None,
            "Mulut": None,
            "Baju": None,
            "Aksesoris": None
        }
    if 'positions' not in st.session_state:
        st.session_state.positions = {
            "Mata": {"x": 0, "y": 0, "scale": 1.0},
            "Mulut": {"x": 0, "y": 0, "scale": 1.0},
            "Aksesoris": {"x": 0, "y": 0, "scale": 1.0}
        }
    if 'adjust_settings' not in st.session_state:
        st.session_state.adjust_settings = {
            "Mata": False,
            "Mulut": False,
            "Aksesoris": True  # Default aktif untuk aksesoris
        }

    # 1. Tampilkan Base Image
    st.subheader("Base Image")
    base_img = load_image("assets/base.png")
    if base_img:
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.image(base_img, use_container_width=True)

    # 2. Pemilihan komponen
    for category in ["Mata", "Mulut", "Baju", "Aksesoris"]:
        st.subheader(f"Pilih {category}")
        
        options = COMPONENTS[category]
        cols = st.columns(5)
        
        for i, (name, path) in enumerate(options.items()):
            with cols[i % 5]:
                if path:
                    img = load_image(path)
                    if img:
                        is_selected = st.session_state.selected[category] == path
                        border_color = "#1E90FF" if is_selected else "transparent"
                        
                        st.markdown(
                            f'<div style="border: 2px solid {border_color}; border-radius: 10px; padding: 5px; display: inline-block;">'
                            f'<img src="data:image/png;base64,{image_to_base64(img)}" width="100" style="cursor: pointer;">'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        
                        if st.button(f"Pilih {name}", key=f"btn_{category}_{name}"):
                            st.session_state.selected[category] = path
                            st.rerun()
                else:
                    if st.button("❌ Hapus", key=f"btn_{category}_none"):
                        st.session_state.selected[category] = None
                        st.rerun()

    # 3. Toggle untuk atur posisi mata/mulut
    for category in ["Mata", "Mulut"]:
        if st.session_state.selected[category]:
            with st.expander(f"⚙️ Atur posisi {category}?", expanded=False):
                st.session_state.adjust_settings[category] = st.checkbox(
                    f"Ya, atur posisi {category}",
                    value=st.session_state.adjust_settings[category],
                    key=f"adjust_{category}"
                )

    # 4. Kontrol posisi dan ukuran
    for category in ["Mata", "Mulut", "Aksesoris"]:
        if st.session_state.selected[category] and (
            category == "Aksesoris" or st.session_state.adjust_settings[category]
        ):
            st.subheader(f"Pengaturan {category}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_x = st.slider(
                    "Posisi Horizontal", -300, 300,
                    st.session_state.positions[category]["x"],
                    key=f"{category}_x"
                )
                st.session_state.positions[category]["x"] = new_x
            
            with col2:
                new_y = st.slider(
                    "Posisi Vertikal", -300, 300,
                    st.session_state.positions[category]["y"],
                    key=f"{category}_y"
                )
                st.session_state.positions[category]["y"] = new_y
            
            with col3:
                new_scale = st.slider(
                    "Ukuran", 0.5, 2.0,
                    st.session_state.positions[category]["scale"], 0.1,
                    key=f"{category}_scale"
                )
                st.session_state.positions[category]["scale"] = new_scale

    # 5. Gabungkan gambar
    if base_img and any(st.session_state.selected.values()):
        result = base_img.copy()
        
        for layer in ["Baju", "Mata", "Mulut", "Aksesoris"]:
            if st.session_state.selected[layer]:
                img = load_image(st.session_state.selected[layer])
                if img:
                    # Apply scaling
                    if layer in ["Mata", "Mulut", "Aksesoris"]:
                        width, height = img.size
                        new_size = (
                            int(width * st.session_state.positions[layer]["scale"]), 
                            int(height * st.session_state.positions[layer]["scale"])
                        )
                        img = img.resize(new_size, Image.LANCZOS)
                    
                    # Apply position
                    x, y = 0, 0
                    if layer in ["Mata", "Mulut"] and st.session_state.adjust_settings[layer]:
                        x = st.session_state.positions[layer]["x"]
                        y = st.session_state.positions[layer]["y"]
                    elif layer == "Aksesoris":
                        x = st.session_state.positions[layer]["x"]
                        y = st.session_state.positions[layer]["y"]
                    
                    result.paste(img, (x, y), img)

        # Tampilkan hasil
        st.subheader("Hasil Akhir")
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.image(result, use_container_width=True)
            
            # Tombol download
            buf = BytesIO()
            result.save(buf, format="PNG")
            st.download_button(
                "⬇️ Download Batsya",
                buf.getvalue(),
                "batsya.png",
                "image/png",
                use_container_width=True
            )

            # Copyright notice - TAMBAHAN BARU
            st.markdown("""
            <div style="text-align: center; margin-top: 20px; color: #666;">
                Thanks to Erlia/Erza, Mie Goreng, beserta para member yang telah membuat gambar-gambar diatas, shout out to them o7.
                \n
                © 2025 TheKnightFox - All Rights Reserved
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")
    main()