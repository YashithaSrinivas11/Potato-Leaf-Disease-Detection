import streamlit as st
from PIL import Image
import numpy as np

st.title("🥔 Potato Leaf Disease Detection")

uploaded_file = st.file_uploader(
    "Upload Potato Leaf Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize((224, 224))
    st.image(image, caption="Uploaded Image")

    img = np.array(image)

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    # ------------------------------------------------
    # STEP 1: Detect LEAF REGION (remove background)
    # ------------------------------------------------
    leaf_mask = (
        (g > 60) &
        (g > r * 0.8) &
        (g > b * 0.8)
    )

    leaf_pixels = np.sum(leaf_mask)

    if leaf_pixels == 0:
        st.error("Leaf not detected properly")
        st.stop()

    # ------------------------------------------------
    # STEP 2: Disease Masks ONLY inside leaf
    # ------------------------------------------------

    # Healthy green
    healthy_mask = leaf_mask & (
        (g > r + 20) &
        (g > b + 20)
    )

    # Early Blight (brown lesions)
    early_mask = leaf_mask & (
        (r > 110) &
        (g < 150) &
        (b < 120)
    )

    # Late Blight (dark infected regions)
    late_mask = leaf_mask & (
        (r < 80) &
        (g < 80) &
        (b < 80)
    )

    healthy_ratio = np.sum(healthy_mask) / leaf_pixels
    early_ratio = np.sum(early_mask) / leaf_pixels
    late_ratio = np.sum(late_mask) / leaf_pixels

    # ------------------------------------------------
    # STEP 3: Classification
    # ------------------------------------------------
    if healthy_ratio > 0.65:
        prediction = "✅ Healthy"
        confidence = healthy_ratio * 100

    elif late_ratio > 0.15:
        prediction = "⚫ Late Blight"
        confidence = late_ratio * 100

    elif early_ratio > 0.10:
        prediction = "🟤 Early Blight"
        confidence = early_ratio * 100

    else:
        prediction = "⚠️ Mild Infection"
        confidence = 75

    # ------------------------------------------------
    # OUTPUT
    # ------------------------------------------------
    st.subheader(f"Prediction: {prediction}")
    st.write(f"Confidence: {confidence:.2f}%")

    with st.expander("Analysis"):
        st.write(f"Healthy Ratio: {healthy_ratio:.2f}")
        st.write(f"Early Blight Ratio: {early_ratio:.2f}")
        st.write(f"Late Blight Ratio: {late_ratio:.2f}")
