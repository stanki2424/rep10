import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Конфигурация на страницата
st.set_page_config(page_title="OCR Ingredient Checker", layout="centered")

# Списък с потенциално вредни съставки
harmful_ingredients = {
    "E621": "Monosodium Glutamate (MSG)",
    "E211": "Sodium Benzoate",
    "E250": "Sodium Nitrite",
    "E951": "Aspartame",
    "E102": "Tartrazine",
    "E110": "Sunset Yellow",
}

# Заглавие
st.title("🔍 OCR Ingredient Checker")
st.write("Upload a product label image to detect harmful ingredients.")

# Качване на файл
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'bg'])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    reader = load_ocr()
    image_np = np.array(image)

    with st.spinner("Reading text..."):
        results = reader.readtext(image_np)

    # Обединяване на текста
    detected_text = " ".join([res[1] for res in results])
    detected_text_upper = detected_text.upper()

    st.subheader("📄 Detected Text")
    st.write(detected_text)

    st.subheader("⚠️ Harmful Ingredients Found")
    found_any = False

    for code, name in harmful_ingredients.items():
        if code in detected_text_upper:
            st.warning(f"{code} - {name}")
            found_any = True

    if not found_any:
        st.success("No harmful ingredients detected from the list ✅")

    # Debug (по желание)
    with st.expander("🔎 Raw OCR Output"):
        st.write(results)
