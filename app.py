from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class Approval:
    def __init__(self, header, value, approval_type):
        self.header = header
        self.value = value
        self.approval_type = approval_type
        self.status = "Pending"
        self.comments = []

    def add_comment(self, user, comment):
        self.comments.append({"user": user.name, "comment": comment})

class ApprovalWorkflow:
    def __init__(self):
        self.users = []
        self.approvals = []

    def add_user(self, name, role):
        user = User(name, role)
        self.users.append(user)
        return user

    def create_approval(self, header, value, approval_type):
        approval = Approval(header, value, approval_type)
        self.approvals.append(approval)
        return approval

    def submit_approval(self, user, approval):
        if user.role == "Final Approver":
            approval.status = "Approved"
        else:
            approval.status = "In Progress"

workflow = ApprovalWorkflow()

@app.route('/')
def index():
    return render_template('index.html', approvals=workflow.approvals)

@app.route('/create_approval', methods=['POST'])
def create_approval():
    header = request.form['header']
    value = int(request.form['value'])
    approval_type = request.form['approval_type']

    approval = workflow.create_approval(header, value, approval_type)

    return redirect(url_for('index'))

@app.route('/submit_approval/<int:approval_id>', methods=['POST'])
def submit_approval(approval_id):
    user_name = request.form['user']
    comment = request.form['comment']

    user = next((u for u in workflow.users if u.name == user_name), None)
    approval = next((a for a in workflow.approvals if a.id == approval_id), None)

    if user and approval:
        approval.add_comment(user, comment)
        workflow.submit_approval(user, approval)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

