from database_sqlite.models import Submission
import evaluation.evaluation_helper as evaluation_helper
from datetime import datetime
from evaluation.models import SubmitInputModel
from fastapi import UploadFile, File, Form
import zipfile

# @router.post("/submit")
# async def submit(db: db_dependency, submission_file:UploadFile = File(...)):
#     result = []
#     evaluation_helper.check_file_extension(submission_file)
#     temp_zip_path = await evaluation_helper.save_zip_file(submission_file)
#     challenge_folder_name = await evaluation_helper.extract_submission(temp_zip_path)
#     return result

async def submit(db, description, challenge_title, submitter, submission_file:UploadFile = File(...)):
    evaluation_helper.check_challenge_title(challenge_title)
    submitter = evaluation_helper.check_submitter(submitter)
    description = evaluation_helper.check_description(description)

    print(description)

    print(submission_file)

    print(submitter)

    print(challenge_title)



    # dev_out = requests.get(repo_url + "/raw/branch/master/dev-0/out.tsv").text
    # test_out = requests.get(repo_url + "/raw/branch/master/test-A/out.tsv").text
    # dev_result = dev_out.replace('\r', '').split('\n')[0]
    # test_result = test_out.replace('\r', '').split('\n')[0]
    required_files = ["README.md", "dev-0/expected.tsv", "test-A/expected.tsv"]
    # with zipfile.ZipFile(submission_file, 'r') as zip_ref:
    #     submission_title = zip_ref.filelist[0].filename[:-1]
    #     print(submission_title)


    when = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    create_submission_model = Submission(
        challenge = "challenge_title",
        submitter = "submitter",
        description = description,
        dev_result = "dev_result",
        test_result = "test_result",
        when = when,
    )
    db.add(create_submission_model)
    db.commit()
    return {"success": True, "submission": "description", "message": "Submission added successfully"}

async def get_metrics():
    result =  [{"name": "Accuracy"}, {"name": "Precision"}]
    return result

async def get_all_submissions(db, challenge: str):
    result = []
    submissions = db.query(Submission).where(Submission.challenge == challenge)
    for submission in submissions:
        result.append({
            "id": submission.id,
            "submitter": submission.submitter,
            "description": submission.description,
            "dev_result": submission.dev_result,
            "test_result": submission.test_result,
            "when": submission.when,
        })
    return result