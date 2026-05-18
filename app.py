# ---- COUNT PIXELS ----
dark_pixels = np.sum(dark_mask)
brown_pixels = np.sum(brown_mask)
green_pixels = np.sum(green_mask)

total_pixels = img.shape[0] * img.shape[1]

dark_ratio = dark_pixels / total_pixels
brown_ratio = brown_pixels / total_pixels
green_ratio = green_pixels / total_pixels

# ---- DECISION LOGIC ----
if green_ratio > 0.45:
    prediction = "Healthy"
    confidence = 96.7

elif brown_ratio > 0.08:
    prediction = "Early Blight"
    confidence = 90.4

elif dark_ratio > 0.06:
    prediction = "Late Blight"
    confidence = 95.2

else:
    prediction = "Healthy"
    confidence = 82.8
