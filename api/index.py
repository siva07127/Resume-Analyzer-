from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

skills_list = [
    'python',
    'java',
    'c',
    'c++',
    'html',
    'css',
    'javascript',
    'mysql',
    'django',
    'flask',
    'react',
    'nodejs',
    'machine learning',
    'data science',
    'sql',
    'git',
    'github'
]

job_roles = {

    'Python Developer': [
        'python',
        'flask',
        'django',
        'sql'
    ],

    'Frontend Developer': [
        'html',
        'css',
        'javascript',
        'react'
    ],

    'Data Scientist': [
        'python',
        'machine learning',
        'data science'
    ],

    'Full Stack Developer': [
        'html',
        'css',
        'javascript',
        'python',
        'mysql'
    ]
}


def extract_text_from_pdf(pdf_path):

    text = ''

    reader = PdfReader(pdf_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text.lower()


@app.route('/', methods=['GET', 'POST'])

def index():

    extracted_skills = []
    score = 0
    suggestions = []
    matched_jobs = []

    if request.method == 'POST':

        file = request.files['resume']

        if file:

            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                file.filename
            )

            file.save(filepath)

            resume_text = extract_text_from_pdf(filepath)

            for skill in skills_list:

                if skill in resume_text:
                    extracted_skills.append(skill)

            score = min(
                len(extracted_skills) * 5,
                100
            )

            if score < 30:

                suggestions.append(
                    'Add more technical skills.'
                )

                suggestions.append(
                    'Include internships or projects.'
                )

                suggestions.append(
                    'Improve resume formatting.'
                )

            elif score < 60:

                suggestions.append(
                    'Add certifications.'
                )

                suggestions.append(
                    'Mention GitHub projects.'
                )

            else:

                suggestions.append(
                    'Excellent resume.'
                )

                suggestions.append(
                    'Ready for placements.'
                )

            for role, required_skills in job_roles.items():

                matched = 0

                for skill in required_skills:

                    if skill in extracted_skills:
                        matched += 1

                if matched >= 2:
                    matched_jobs.append(role)

    return render_template(
        'index.html',
        skills=extracted_skills,
        score=score,
        suggestions=suggestions,
        jobs=matched_jobs
    )


if __name__ == '__main__':
    app.run(debug=True)