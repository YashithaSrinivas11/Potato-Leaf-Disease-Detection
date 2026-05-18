import streamlit as st
from PIL import Image
import numpy as np

# ---------------- UI ----------------
st.title("🥔 Potato Leaf Disease Detection")
st.write("Upload a potato leaf image to detect disease")

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- PROCESS IMAGE ----------------
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize((224, 224))

    st.image(image, caption="Uploaded Image", use_column_width=True)

    img = np.array(image)

    # Split RGB channels
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    # ---------------- MASKS ----------------

    # Healthy Green Pixels
    green_mask = (
        (g > r + 25) &
        (g > b + 25) &
        (g > 90)
    )

    # Early Blight (Brown Spots)
    brown_mask = (
        (r > 100) & (r < 200) &
        (g > 60) & (g < 150) &
        (b < 120)
    )

    # Late Blight (Dark Necrotic Regions)
    dark_mask = (
        (r < 70) &
        (g < 70) &
        (b < 70)
    )

    # ---------------- COUNT PIXELS ----------------
    green_pixels = np.sum(green_mask)
    brown_pixels = np.sum(brown_mask)
    dark_pixels = np.sum(dark_mask)

    total_pixels = img.shape[0] * img.shape[1]

    # Convert to percentage (VERY IMPORTANT)
    green_ratio = green_pixels / total_pixels
    brown_ratio = brown_pixels / total_pixels
    dark_ratio = dark_pixels / total_pixels

    # ---------------- DECISION LOGIC ----------------
    if green_ratio > 0.45:
        prediction = "✅ Healthy Leaf"
        confidence = green_ratio * 100

    elif brown_ratio > 0.08:
        prediction = "🟤 Early Blight"
        confidence = brown_ratio * 100

    elif dark_ratio > 0.06:
        prediction = "⚫ Late Blight"
        confidence = dark_ratio * 100

    else:
        prediction = "⚠️ Unable to classify clearly"
        confidence = 70

    # ---------------- OUTPUT ----------------
    st.subheader(f"Prediction: {prediction}")
    st.write(f"Confidence: {confidence:.2f}%")

    # Optional Debug Info (Great for Viva)
    with st.expander("Show Analysis"):
        st.write(f"Green Ratio: {green_ratio:.2f}")
        st.write(f"Brown Ratio: {brown_ratio:.2f}")
        st.write(f"Dark Ratio: {dark_ratio:.2f}")
