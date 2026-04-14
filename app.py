import streamlit as st
import pandas as pd
import csv
import io

st.set_page_config(page_title="CSV Formatter", layout="wide")
st.title("🛠️ Greek CSV Auto-Formatter")

uploaded_file = st.file_uploader("Ανεβάστε το CSV αρχείο σας", type=['csv'])

if uploaded_file is not None:
    # --- STEP 1: DETECTION (Ανίχνευση Διαχωριστή) ---
    try:
        # Διαβάζουμε το δείγμα από τα bytes του uploaded_file
        sample_bytes = uploaded_file.read(4096)
        sample_text = sample_bytes.decode('cp1253')
        
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample_text, delimiters=[',', ';', '\t', '|'])
        detected_delimiter = dialect.delimiter
        
        # Επαναφέρουμε τον κέρσορα του αρχείου στην αρχή για να το διαβάσει η pandas
        uploaded_file.seek(0)
        
        st.info(f"Ανιχνεύθηκε διαχωριστής: `{detected_delimiter}`")
    except Exception as e:
        detected_delimiter = ';' 
        uploaded_file.seek(0)
        st.warning(f"Ο αυτόματος εντοπισμός απέτυχε. Χρήση default: `;`")

    # --- STEP 2: READ (Διάβασμα) ---
    try:
        df = pd.read_csv(
            uploaded_file, 
            encoding='cp1253', 
            sep=detected_delimiter, 
            on_bad_lines='warn', 
            engine='python'
        )
        
        st.subheader("Προεπισκόπηση Δεδομένων")
        st.dataframe(df.head(10))

        # --- STEP 3: SAVE & DOWNLOAD (Εξαγωγή) ---
        # Μετατροπή σε comma-separated CSV για το Shopify/Magento
        output_data = df.to_csv(index=False, encoding='cp1253', sep=',')
        
        st.download_button(
            label="📥 Κατέβασμα Ενημερωμένου CSV",
            data=output_data,
            file_name=f"updated_{uploaded_file.name}",
            mime='text/csv'
        )
        st.success("Το αρχείο είναι έτοιμο!")

    except Exception as e:
        st.error(f"Μοιραίο σφάλμα: {e}")

