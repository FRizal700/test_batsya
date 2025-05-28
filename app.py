import streamlit as st
from PIL import Image
from io import BytesIO
import os
import base64
import time

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
    "Glassess": {
        "g1": "assets/g1.webp",
        "g2": "assets/g2.webp",
        "g3": "assets/g3.webp",
        "g4": "assets/g4.webp",
        "g5": "assets/g5.webp",
        "None": None
    },
    "Topi": {
        "t1": "assets/t1.webp",
        "t2": "assets/t2.webp",
        "t3": "assets/t3.webp",
        "t4": "assets/t4.webp",
        "t5": "assets/t5.webp",
        "t6": "assets/t6.webp",
        "t7": "assets/t7.webp",
        "None": None
    },
    "Lightstick Kanan": {
        "lsr1": "assets/lsr1.webp",
        "lsr2": "assets/lsr2.webp",
        "lsr3": "assets/lsr3.webp",
        "lsr4": "assets/lsr4.webp",
        "lsr5": "assets/lsr5.webp",
        "lsr6": "assets/lsr6.webp",
        "lsr7": "assets/lsr7.webp",
        "lsr8": "assets/lsr8.webp",
        "lsr9": "assets/lsr9.webp",
        "None": None
    },
    "Lightstick Kiri": {
        "lsl1": "assets/lsl1.webp",
        "lsl2": "assets/lsl2.webp",
        "lsl3": "assets/lsl3.webp",
        "lsl4": "assets/lsl4.webp",
        "lsl5": "assets/lsl5.webp",
        "lsl6": "assets/lsl6.webp",
        "lsl7": "assets/lsl7.webp",
        "lsl8": "assets/lsl8.webp",
        "lsl9": "assets/lsl9.webp",
        "None": None
    },
    "FanKiri": {
        "fs1": "assets/fs1.webp",
        "fs2": "assets/fs2.webp",
        "fs3": "assets/fs3.webp",
        "None": None
    },
    "FanKanan": {
        "fs1": "assets/fs1.webp",
        "fs2": "assets/fs2.webp",
        "fs3": "assets/fs3.webp",
        "None": None
    }
}

# Posisi default untuk lightstick
DEFAULT_LS_POSITIONS = {
    "Lightstick Kanan": {"x": 321, "y": 107, "scale": 0.50, "rotation": 8},
    "Lightstick Kiri": {"x": -64, "y": 107, "scale": 0.50, "rotation": -8},
    "FanKiri": {"x": -98, "y": 19, "scale": 0.50, "rotation": 28},
    "FanKanan": {"x": 292, "y": 19, "scale": 0.50, "rotation": -28} 
}

# Cache untuk gambar yang sudah dimuat
IMAGE_CACHE = {}

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def load_image(path):
    if path is None:
        return None
        
    if path in IMAGE_CACHE:
        return IMAGE_CACHE[path]
        
    try:
        img = Image.open(path).convert("RGBA")
        IMAGE_CACHE[path] = img  # Cache the image
        return img
    except Exception as e:
        st.error(f"Gagal memuat gambar {path}: {str(e)}")
        return None

def rotate_image(image, angle):
    """Rotate image by given angle (in degrees) and return the rotated image with transparent background maintained."""
    if angle == 0:
        return image
    return image.rotate(angle, expand=True, resample=Image.BICUBIC)

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
            "Glassess": None,
            "Topi": None,
            "Lightstick Kanan": None,
            "Lightstick Kiri": None,
            "FanKiri": None,
            "FanKanan": None
        }
    if 'positions' not in st.session_state:
        st.session_state.positions = {
            "Mata": {"x": 0, "y": 0, "scale": 1.0, "rotation": 0},
            "Mulut": {"x": 0, "y": 0, "scale": 1.0, "rotation": 0},
            "Glassess": {"x": 4, "y": -101, "scale": 1.0, "rotation": 0},
            "Topi": {"x": 134, "y": -110, "scale": 0.40, "rotation": 0},
            "Lightstick Kanan": DEFAULT_LS_POSITIONS["Lightstick Kanan"],
            "Lightstick Kiri": DEFAULT_LS_POSITIONS["Lightstick Kiri"],
            "FanKiri": DEFAULT_LS_POSITIONS["FanKiri"],
            "FanKanan": DEFAULT_LS_POSITIONS["FanKanan"]
        }
    if 'adjust_settings' not in st.session_state:
        st.session_state.adjust_settings = {
            "Mata": False,
            "Mulut": False,
            "Glassess": True,
            "Topi": True,
            "Lightstick Kanan": False,
            "Lightstick Kiri": False,
            "FanKiri": False,
            "FanKanan": False
        }

    # 1. Tampilkan Base Image
    st.subheader("Base Image")
    base_img = load_image("assets/base.png")
    if base_img:
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.image(base_img, width=400)

    # 2. Pemilihan komponen dengan expander
    for category in ["Mata", "Mulut", "Baju", "Glassess", "Topi", "Lightstick Kiri", "Lightstick Kanan", "FanKiri", "FanKanan"]:
        with st.expander(f"🔘 Pilih {category}", expanded=False):
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
                                # Set default position for lightsticks
                                if category in ["Lightstick Kiri", "Lightstick Kanan", "FanKiri", "FanKanan"]:
                                    st.session_state.positions[category] = DEFAULT_LS_POSITIONS[category].copy()
                                st.rerun()
                    else:
                        if st.button("❌ Hapus", key=f"btn_{category}_none"):
                            st.session_state.selected[category] = None
                            st.rerun()

    # 3. Toggle untuk atur posisi
    for category in ["Mata", "Mulut", "Glassess", "FanKiri", "FanKanan"]:
        if st.session_state.selected[category]:
            with st.expander(f"⚙️ Atur posisi {category}?", expanded=False):
                st.session_state.adjust_settings[category] = st.checkbox(
                    f"Ya, atur posisi {category}",
                    value=st.session_state.adjust_settings[category],
                    key=f"adjust_{category}"
                )

    # 4. Kontrol posisi, ukuran, dan rotasi
    for category in ["Mata", "Mulut", "Glassess", "Topi", "FanKiri", "FanKanan"]:
        if st.session_state.selected[category] and (
            category in ["Glassess", "Topi", "Fan"] or st.session_state.adjust_settings[category]
        ):
            st.subheader(f"Pengaturan {category}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                new_x = st.slider(
                    "Posisi Horizontal", -400, 400,
                    st.session_state.positions[category]["x"],
                    key=f"{category}_x"
                )
                st.session_state.positions[category]["x"] = new_x
            
            with col2:
                new_y = st.slider(
                    "Posisi Vertikal", -400, 400,
                    st.session_state.positions[category]["y"],
                    key=f"{category}_y"
                )
                st.session_state.positions[category]["y"] = new_y
            
            with col3:
                new_scale = st.slider(
                    "Ukuran", 0.1, 3.0,
                    st.session_state.positions[category]["scale"], 0.1,
                    key=f"{category}_scale"
                )
                st.session_state.positions[category]["scale"] = new_scale
                
            with col4:
                if category in ["Lightstick Kiri", "Lightstick Kanan", "FanKiri", "FanKanan"]:
                    new_rotation = st.slider(
                        "Rotasi", -180, 180,
                        st.session_state.positions[category]["rotation"],
                        key=f"{category}_rotation"
                    )
                    st.session_state.positions[category]["rotation"] = new_rotation

    # 5. Gabungkan gambar
    if base_img and any(st.session_state.selected.values()):
        start_time = time.time()
        
        # Tambahkan padding di atas (150px) dan samping (100px)
        padded_width = base_img.width + 200  # 100 kiri + 100 kanan
        padded_height = base_img.height + 200  # 150 atas + 50 bawah
        result = Image.new("RGBA", (padded_width, padded_height), (0, 0, 0, 0))
        
        # Posisikan base image di tengah dengan padding atas lebih besar
        base_x = 100  # Padding kiri
        base_y = 150  # Padding atas
        result.paste(base_img, (base_x, base_y), base_img)
        
        # Urutan layer
        layer_order = ["Baju", "Mata", "Mulut", "Glassess", "Topi", "FanKiri", "FanKanan", "Lightstick Kiri", "Lightstick Kanan"]
        
        for layer in layer_order:
            if st.session_state.selected[layer]:
                img = load_image(st.session_state.selected[layer])
                if img:
                    # Apply scaling
                    if layer in st.session_state.positions:
                        width, height = img.size
                        scale = st.session_state.positions[layer]["scale"]
                        new_size = (int(width * scale), int(height * scale))
                        img = img.resize(new_size, Image.LANCZOS)
                    
                    # Apply rotation (khusus untuk lightstick)
                    if layer in st.session_state.positions and "rotation" in st.session_state.positions[layer]:
                        rotation = st.session_state.positions[layer]["rotation"]
                        img = rotate_image(img, rotation)
                    
                    # Apply position (ditambahkan offset base image)
                    if layer in st.session_state.positions:
                        x = st.session_state.positions[layer]["x"] + base_x
                        y = st.session_state.positions[layer]["y"] + base_y
                    else:
                        x, y = base_x, base_y
                    
                    result.paste(img, (x, y), img)

        # Tampilkan hasil
        st.subheader("Hasil Akhir")
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.image(result, width=500)
            
            # Tombol download
            buf = BytesIO()
            result.save(buf, format="PNG")
            st.download_button(
                "⬇️ Download Batsya",
                buf.getvalue(),
                "batsya.png",
                "image/png"
            )

            # Debug info
            st.text(f"Waktu proses: {time.time() - start_time:.2f} detik")
            
            # Copyright notice
            st.markdown("""
            <div style="text-align: center; margin-top: 20px; color: #666;">
                Thanks to Erlia/Erza, Mie Goreng, beserta para member yang telah membantu, shout out to them o7.
                \n
                © 2025 TheKnightFox - All Rights Reserved
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")
    main()