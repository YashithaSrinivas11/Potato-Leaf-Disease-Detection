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
    # STEP 1 — Detect PLANT REGION (not only green)
    # ------------------------------------------------
    plant_mask = (
        (r > 40) | (g > 40) | (b > 40)
    )

    plant_pixels = np.sum(plant_mask)

    # ------------------------------------------------
    # STEP 2 — Disease Detection
    # ------------------------------------------------

    # Healthy Green Pixels
    healthy_mask = plant_mask & (
        (g > r + 20) &
        (g > b + 20)
    )

    # Early Blight (brown lesions)
    early_mask = plant_mask & (
        (r > 110) &
        (g > 60) &
        (g < 150) &
        (b < 120)
    )

    # Late Blight (dark infected areas)
    late_mask = plant_mask & (
        (r < 90) &
        (g < 90) &
        (b < 90)
    )

    healthy_ratio = np.sum(healthy_mask) / plant_pixels
    early_ratio = np.sum(early_mask) / plant_pixels
    late_ratio = np.sum(late_mask) / plant_pixels

    # ------------------------------------------------
    # STEP 3 — FINAL CLASSIFICATION
    # ------------------------------------------------
    if late_ratio > 0.18:
        prediction = "⚫ Late Blight"
        confidence = late_ratio * 100

    elif early_ratio > 0.12:
        prediction = "🟤 Early Blight"
        confidence = early_ratio * 100

    elif healthy_ratio > 0.35:
        prediction = "✅ Healthy"
        confidence = healthy_ratio * 100

    else:
        prediction = "⚠️ Mixed Infection"
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
