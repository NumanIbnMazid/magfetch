
============== TODO ==============
#   Paginate Announcement
#   Important Task/Notification after passing 10 days of commenting
#   File Save Naming Convention: username_file_category
#   After submitting contribution email, system notification
#   Danger zone if not commented within 10 days
#   Rating Contributions, later search by rating and select for magazine
#	Marketing Manager can view the comments and all the process
#	Update EEE marketing manager email
#	Administrator can view the suspicious users

============== TODO TOMMOROW ==============
# Notification Display
# What if upload Multiple file? Delete Code to Delete Previous Uploads
# Uploaded File List, Detail, Update View
# Who can Delete Uploaded file ? Student or Marketing Coordinator?
# Google Doc to read Document File

============== Questionnaires ==============
# If only Marketing coordinator can access all contributions???
# Should Marketing Manager able to download selected contributions as zip only after final closure date???

============== DOC ==============
# 2.	Evaluation of Team - baki...........
# Default comment strength
# Appendix-
	* Check contribution from email
	* Check Doc file with google doc

===
# add code on pythonanywhere.py:
# ==================== Security Modules ===================
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 300  # set low, but when site is ready for deployment, set to at least 15768000 (6 months)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Allowed Hosts
#ALLOWED_HOSTS=localhost,127.0.0.1, magfetch.pythonanywhere.com, magfetch.herokuapp.com, .magfetch.com
ALLOWED_HOSTS=magfetch.pythonanywhere.com

#	Marketing Manager can view the comments and all the process
#	Update EEE marketing manager email
#	Administrator can view the suspicious users
# 	Add to manage terms and conditions
