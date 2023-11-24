from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class Approval:
    def __init__(self, header, value, approval_type):
        self.id = str(uuid.uuid4())
        self.header = header
        self.value = value
        self.approval_type = approval_type
        self.status = "Pending"
        self.comments = []
        self.workflow_type = None  

    def add_comment(self, user, comment):
        self.comments.append({"user": user.name, "comment": comment})

class ApprovalWorkflow:
    def __init__(self):
        self.users = []
        self.approvals = []

    def add_user(self, name, role):
        user = User(name, role)
        self.users.append(user)

    def create_approval(self, header, value, approval_type):
        approval = Approval(header, value, approval_type)
        self.approvals.append(approval)
        self.set_workflow_type(approval)  
        return approval

    def set_workflow_type(self, approval):
        # Logic to set the workflow type based on approval criteria
        if approval.value > 10000:
            approval.workflow_type = "Workflow 3"
        elif approval.value > 1000:
            approval.workflow_type = "Workflow 2"
        elif approval.value > 100:
            approval.workflow_type = "Workflow 1"
        else:
            approval.workflow_type = "Approval Type Workflow"

    def submit_approval(self, approval, user, comment):
        approval.add_comment(user, comment)

workflow = ApprovalWorkflow()
workflow.add_user("Aarav", "Approver")
workflow.add_user("Priya", "Approver")
workflow.add_user("Rajesh", "Approver")
workflow.add_user("Sunita", "Approver")
workflow.add_user("Mohan", "Final Approver")

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html', approvals=workflow.approvals)

# Route for submitting a new approval
@app.route('/submit_approval', methods=['POST'])
def submit_approval():
    header = request.form['header']
    value = int(request.form['value'])
    approval_type = request.form['approval_type']
    current_user = workflow.users[0]
    new_approval = workflow.create_approval(header, value, approval_type)
    workflow.submit_approval(new_approval, current_user, "Submitted for approval")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
