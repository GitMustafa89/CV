import streamlit as st #streamlit for making website
import pickle #for loading datasets
import re #regular expression data cleaning
import nltk
import os

port = int(os.environ.get('PORT', 8000))

nltk.download('punkt')
nltk.download('stopwords')

#loading models
clf = pickle.load(open('clf.pkl','rb'))
tfidfd = pickle.load(open('tfidf.pkl','rb')) #rb-readbinary mode

#cleaning resume
def cleaning(text):
    pattern = re.compile(r'https?://\S+|www\.\S+')
    pattern = re.compile(r'@\S+')
    pattern = re.compile(r'RT|cc')
    pattern = re.compile(r'#\S+')
    pattern = re.compile(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""))
    pattern = re.compile(r'[^\x00-\x7f]')
    pattern = re.compile(r'\s+')
    return pattern.sub(r'', text)


#web app
def main():
    st.title("Resume Screening App")
    uploaded_file=st.file_uploader('Upload Resume',type=['txt','pdf','doc'])

    if uploaded_file is not None:
        try:
            resume_bytes = uploaded_file.read() #converting into bytes
            resume_text = resume_bytes.decode('utf-8') #then decode into utf-8
        except UnicodeDecodeError:
            # If UTF-8 decoding fails, try decoding with 'latin-1'
            resume_text = resume_bytes.decode('latin-1')

        cleaned_resume = cleaning(resume_text)
        input_features = tfidfd.transform([cleaned_resume])
        prediction_id = clf.predict(input_features)[0]
        st.write(prediction_id)

        # Map category ID to category name
        category_mapping = {
            15: "Java Developer",
            23: "Testing",
            8: "DevOps Engineer",
            20: "Python Developer",
            24: "Web Designing",
            12: "HR",
            13: "Hadoop",
            3: "Blockchain",
            10: "ETL Developer",
            18: "Operations Manager",
            6: "Data Science",
            22: "Sales",
            16: "Mechanical Engineer",
            1: "Arts",
            7: "Database",
            11: "Electrical Engineering",
            14: "Health and fitness",
            19: "PMO",
            4: "Business Analyst",
            9: "DotNet Developer",
            2: "Automation Testing",
            17: "Network Security Engineer",
            21: "SAP Developer",
            5: "Civil Engineer",
            0: "Advocate",
        }

        category_name = category_mapping.get(prediction_id, "Unknown")

        st.write("Predicted Category:", category_name)


#python_main
if __name__ == "__main__":
    main()














