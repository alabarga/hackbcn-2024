# DocLingo: Decoding Medical Jargon with AI
![doclingo_logo](https://github.com/alabarga/hackbcn-2024/assets/166339/38208f52-e7a0-4a94-891e-ad82ed7af5b5)
**DocLingo** is an innovative app designed to bridge the communication gap between healthcare professionals and patients. 🏥 By enabling doctors to query their databases using natural language, the app simplifies the retrieval and analysis of medical data 📊, can automatically generate clinical reports 📝 and translate complex medical terminology into easy-to-understand language. 🗣️ This feature enhances doctor-patient communication 👩‍⚕️👨‍⚕️, ensuring that patients fully comprehend their health information, leading to better informed decisions and improved healthcare outcomes. 💡

## 🚀 Main Objectives
1. **Improve Communication:** Bridge the communication gap between healthcare professionals and patients.
2. **Simplify Data Retrieval:** Allow doctors to query their databases using natural language for easier retrieval and analysis of medical data.
3. **Automate Report Generation:** Automatically generate clinical reports to save time and enhance efficiency.
4. **Simplify Medical Terminology:** Translate complex medical terms into easy-to-understand language for patients.
5. **Enhance Understanding:** Ensure patients fully understand their health information.
6. **Promote Informed Decisions:** Help patients make better informed decisions regarding their health.
7. **Improve Healthcare Outcomes:** Lead to better healthcare outcomes through enhanced doctor-patient communication and understanding.

---

## 📊 AI Technologies used

-  🧪 Model to extract medical entities for training: https://huggingface.co/HMHMlee/BioLinkBERT-base-finetuned-ner
-  🧪 Fine tuned language model for text-to-SQL generation: https://vanna.ai/
-  🧪 Fine-tuned model for entity to clinical report generation: https://mistral.ai/
-  🧪 Language model for report summarization: https://mistral.ai/
-  🤖 Streamlit for user interface: https://streamlit.io/

---

## 📁 Data

In order to train the models and populate the database, we used the following datasources:
- Medical Notes (in spanish): https://zenodo.org/records/7614764
- Structures Data Sythea Project (syhthetic data): https://synthetichealth.github.io/synthea/

---

## 🎨 Slides
- https://docs.google.com/presentation/d/1nSeTjMvAzp2hQKKlFSbaKfW3_K9G95MyhuRO4QniKqw/edit#slide=id.g2e93379d1b9_0_261


---

> Please note that this project is in its MVP stage. While the application has been developed with trained models, there may still be areas that require further improvement and integration. It's important to consider that this development was completed within 36 hours from inception.

---

