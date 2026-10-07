import os
from app import create_app
from app.extensions import db
from app.models import User, UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'UserProfile': UserProfile,
        'Announcement': Announcement,
        'Complaint': Complaint,
        'MessMenu': MessMenu,
        'MessReview': MessReview,
        'Resource': Resource,
        'LostAndFound': LostAndFound
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
