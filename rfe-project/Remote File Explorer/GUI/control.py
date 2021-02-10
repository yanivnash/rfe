# testing
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = 'yanivnash@gmail.com'
reset_code = 'yyyyyyyyyy'

sender_email = 'rfe.noreply@gmail.com'  # sending email
password = 'RFE123456789'  # sending email's password
send_to_email = email  # receiving email
subject = 'Your Password Reset Code'
messageHTML = f"""
<body style="text-align:center; background-color:#e9eed6;">
<h1>Your password reset code is:</h1>
<h1><span style="color: #496dd0">{reset_code}</span></h1>
<h1>Go back to the "Remote File Explorer" app and use that code to reset your password and log back in to your account</h1>
<img src="https://lh3.googleusercontent.com/2QK_cbYd6SuA40L7yDJLNjFtPZjRD_dfKnkdGgz_eRaxTitPpZ05JWhTLK-ulXJxlVBHvKQbTanpM9-ggFon6N0FtWGYxLxo_M2pVZiVVY24m489MogPnwmYtz6gGSlb1Ek4aQbVn0sVfYwgyivdircbkbEHF9G5lU8RlYhngrCFLyVdQU1tqWkdnQ7VcFqscB3iDpQubRTgoEZ9IkBum3UQg9HCw9e2yGny3Wccx_exVn2lr0g3oWMwCMlrqlrEtb59L0l9ME3-uBvz0DV-uECeFLOzHgUTcM2Bq-_l8Y6xZku9IjHlZG39q2cVe9HTs-842X0CH2D-btw6PKLzKqm8XN6J1UHuv5AgbW_DakD5ueFKykoVUipfry4ikUtVCmfx96_oTU3ksvOrTvGZZrRimvY-vwDkzbITSSwHwH6BG6h25ok4z7XAvJqtbSQQVmF1H5NIhKKuW4M4Z5ilKcX4fJF-a2u0azJYa62cyEVjJ6jbzo3wDa_uRluVAXYBy4XOMEo4fLZtXQlASRGnbpfDX5aO-yroEPYJvn8GZqF79NfX3lcg91N_z0UF_9MdiT8yPC7cRHECkGDMKCHFMO0mteGAsXTtdplBtzy1Cp4DbyglvJeCuBWzKhpowQptJYrGPQWdoi79cR3EqxIwECP9oqTD8NEpEM29XYiex3lS19674fndX3q5kKM3=w200-h163-no?authuser=8" alt="LOGO">
<h3>© Remote File Explorer - Yaniv Nash - 2021</h3>
</body>
"""
messagePlain = f"""
Your password reset code is:
{reset_code}
Go back to the "Remote File Explorer" app and use that code to reset your password and log back in to your account
© Remote File Explorer - Yaniv Nash - 2021
"""

msg = MIMEMultipart('alternative')
msg['From'] = 'Remote File Explorer'
msg['To'] = send_to_email
msg['Subject'] = subject

# Attach both plain and HTML versions
msg.attach(MIMEText(messagePlain, 'plain'))
msg.attach(MIMEText(messageHTML, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
text = msg.as_string()
server.sendmail(sender_email, send_to_email, text)
server.quit()