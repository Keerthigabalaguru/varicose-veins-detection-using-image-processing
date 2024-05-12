from flask import Flask, render_template, request, session, flash, send_file
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import mysql.connector
import base64, os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/EdgeServerLogin')
def EdgeServerLogin():
    return render_template('EdgeServerLogin.html')


@app.route('/TTPLogin')
def TTPLogin():
    return render_template('TTPLogin.html')


@app.route('/HealthCareLogin')
def HealthCareLogin():
    return render_template('HealthCareLogin.html')


@app.route('/NewHealthCare')
def NewHealthCare():
    return render_template('NewHealthCare.html')


@app.route("/ttplogin", methods=['GET', 'POST'])
def ttplogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where status='waiting'")
            data = cur.fetchall()

            return render_template('TTPHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('TTPLogin.html')


@app.route("/TTPHome")
def TTPHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting' ")
    data = cur.fetchall()
    return render_template('TTPHome.html', data=data)


@app.route("/RejectInfo")
def TRejectInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='Rejected' ")
    data = cur.fetchall()
    return render_template('TRejectInfo.html', data=data)


@app.route("/ApprovedInfo")
def TApprovedInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='Approved' ")
    data = cur.fetchall()
    return render_template('TApprovedInfo.html', data=data)


@app.route("/Approved")
def Approved():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='Approved' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()
    flash("Health Care  Approved!")
    return render_template('TTPHome.html', data=data)


@app.route("/Reject")
def Reject():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("Update regtb set Status='Rejected' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where status='waiting'")
    data = cur.fetchall()
    flash("Health Care   Rejected!")
    return render_template('TTPHome.html', data=data)


@app.route("/serverlogin", methods=['GET', 'POST'])
def serverlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()

            return render_template('ESeverHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('ESeverHome.html')

@app.route("/ESeverHome")
def ESeverHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('ESeverHome.html', data=data)


@app.route("/ESeverFileInfo")
def ESeverFileInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb  ")
    data = cur.fetchall()
    return render_template('ESeverFileInfo.html', data=data)

@app.route("/EdgeServerrequest")
def EdgeServerrequest():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb  ")
    data = cur.fetchall()
    return render_template('EdgeServerrequest.html', data=data)

@app.route("/newhealth", methods=['GET', 'POST'])
def newhealth():
    if request.method == 'POST':
        name = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        website = request.form['website']
        address = request.form['Address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + website + "','" + address + "','" + username + "','" + password + "','waiting')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('NewHealthCare.html')


@app.route("/hclogin", methods=['GET', 'POST'])
def hclogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['hname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            return render_template('index.html')
            return 'Username or Password is wrong'
        else:
            status = data[8]

            if status == 'waiting':
                flash("waiting for TTP Approved")
                return render_template('HealthCareLogin.html', data=data)
            elif status == 'Rejected':

                flash(" Approved Rejected")
                return render_template('HealthCareLogin.html', data=data)

            else:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM regtb where username='" + username + "' and password='" + password + "'")
                data = cur.fetchall()

                flash("you are successfully logged in")
                return render_template('HealthCareHome.html', data=data)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        from stegano import lsb
        from PIL import Image

        name = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        ano = request.form['ano']
        address = request.form['Address']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)
        import tensorflow as tf
        classifierload = tf.keras.models.load_model('model1.h5')
        import numpy as np
        from keras.preprocessing import image
        test_image = image.load_img("static/upload/" + savename, target_size=(200, 200))
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierload.predict(test_image)

        out = ''
        pre = ''
        if result[0][0] == 1:
            out = "Normal"
            pre = "Nil"
        elif result[0][1] == 1:
            out = "Varicose"
            pre = "Drugs used to treat Varicose Veins ; Expand current row for information about polidocanol polidocanol, 4.7, 3 reviews for polidocanol to treat Varicose Veins."


        hidedata = "DiseaseName :" + out + "  prescription :" + pre

        image = Image.open("./static/upload/" + savename)
        print(f"Original size : {image.size}")  # 5464x3640

        sunset_resized = image.resize((400, 400))
        sunset_resized.save("./static/upload/" + savename)

        secret = lsb.hide("./static/upload/" + savename, hidedata)

        pathname, extension = os.path.splitext("./static/upload/" + savename)
        filename = pathname.split('/')
        imageName = filename[-1] + ".png"
        sname = filename[-1]
        secret.save("./static/Encode/" + imageName)

        savedir = 'static/Split/'
        filename = "./static/Encode/" + imageName
        img = Image.open(filename)
        width, height = img.size
        start_pos = start_x, start_y = (0, 0)
        cropped_image_size = w, h = (200, 200)

        frame_num = 1
        for col_i in range(0, width, w):
            for row_i in range(0, height, h):
                crop = img.crop((col_i, row_i, col_i + w, row_i + h))
                save_to = os.path.join(savedir, sname + "_{:02}.png")
                crop.save(save_to.format(frame_num))
                frame_num += 1

        secp_k = generate_key()
        privhex = secp_k.to_hex()
        pubhex = secp_k.public_key.format(True).hex()

        filepath1 = "./static/Split/" + sname + "_01.png"
        filepath2 = "./static/Split/" + sname + "_02.png"
        filepath3 = "./static/Split/" + sname + "_03.png"
        filepath4 = "./static/Split/" + sname + "_04.png"

        newfilepath1 = "./static/Encrypt/" + sname + "_01.png"
        newfilepath2 = "./static/Encrypt/" + sname + "_02.png"
        newfilepath3 = "./static/Encrypt/" + sname + "_03.png"
        newfilepath4 = "./static/Encrypt/" + sname + "_04.png"

        data1 = 0
        data2 = 0
        data3 = 0
        data4 = 0

        with open(filepath1, "rb") as File:
            data1 = base64.b64encode(File.read())  # convert binary to string data to read file

        with open(filepath2, "rb") as File:
            data2 = base64.b64encode(File.read())

        with open(filepath3, "rb") as File:
            data3 = base64.b64encode(File.read())
        with open(filepath4, "rb") as File:
            data4 = base64.b64encode(File.read())

        print("Private_key:", privhex, "\nPublic_key:", pubhex, "Type: ", type(privhex))

        if (privhex == 'null'):
            flash('Please Choose Another File,file corrupted!')
            return render_template('Hupload.html')

        else:
            encrypted_secp = encrypt(pubhex, data1)
            with open(newfilepath1, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data2)
            with open(newfilepath2, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data3)
            with open(newfilepath3, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            encrypted_secp = encrypt(pubhex, data4)
            with open(newfilepath4, "wb") as EFile:
                EFile.write(base64.b64encode(encrypted_secp))

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO filetb VALUES ('','" + session[
                    'hname'] + "','" + name + "','" + mobile + "','" + email + "','" + ano + "','" + address + "','" + sname + "','" + savename + "','" + pubhex + "','" + privhex + "')")
            conn.commit()
            conn.close()
            flash(hidedata)

        return render_template('HUploadIfo.html', iname=savename, pre=hidedata, sname=sname, pvkey=privhex)


@app.route('/Upload')
def Upload():
    return render_template('HUpload.html')


@app.route('/UploadInfo')
def UploadInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb where HCName='" + session['hname'] + "' ")
    data = cur.fetchall()
    return render_template('HVUploadInfo.html', data=data)


@app.route("/View")
def View():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM filetb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        fid = data[8]

    else:
        return 'Incorrect username / password !'

    from stegano import lsb
    clear_message = lsb.reveal("static/Encode/"+fid)
    session['dfid'] = fid

    org = 'static/upload/'+fid

    print(clear_message)
    return render_template('Hview.html', iname=org,pre=clear_message )


@app.route("/hdown", methods=['GET', 'POST'])
def hdown():
    if request.method == 'POST':

        return send_file('static/upload/' + session['dfid'], as_attachment=True)

@app.route('/HSendrequest')
def HSendrequest():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb where HCName !='" + session['hname'] + "' ")
    data = cur.fetchall()
    return render_template('HSendrequest.html', data=data)

@app.route("/send")
def send():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM filetb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        hname = data[1]
        pname = data[2]
        iname = data[8]
        iid = data[7]
        pkey = data[10]
    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO requesttb VALUES ('','" + id + "','" + hname + "','" + pname + "','" + iname + "','" + iid + "','" + pkey + "','" + session['hname'] + "','waiting')")
    conn.commit()
    conn.close()

    flash("Key Request Send")
    return render_template('HSendrequest.html')


@app.route('/HStatus')
def HStatus():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where RHCName ='" + session['hname'] + "' And Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where RHCName ='" + session['hname'] + "' And Status !='waiting' ")
    data1 = cur.fetchall()


    return render_template('HStatus.html', data=data, data1=data1)



@app.route('/HAccept')
def HAccept():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where HCName ='" + session['hname'] + "' And Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where HCName ='" + session['hname'] + "' And Status !='waiting' ")
    data1 = cur.fetchall()

    return render_template('HAccept.html', data=data, data1=data1)




@app.route("/rApproved")
def rApproved():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM requesttb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        pkey = data[6]
        rhcname = data[7]
    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb where  username='" + rhcname + "'")
    data = cursor.fetchone()

    if data:
        mailid = data[3]

    else:
        return 'Incorrect username / password !'

    msg = "Request Id "+id + "  Private key :"+pkey
    sendmsg(mailid ,msg)




    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("Update requesttb set Status='Approved' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where HCName ='" + session['hname'] + "' And Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where HCName ='" + session['hname'] + "' And Status !='waiting' ")
    data1 = cur.fetchall()



    return render_template('HAccept.html', data=data, data1=data1)


@app.route("/rReject")
def rReject():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("Update requesttb set Status='Rejected' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM requesttb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        pkey = data[6]
        rhcname = data[7]
    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM regtb where  username='" + rhcname + "'")
    data = cursor.fetchone()

    if data:
        mailid = data[3]

    else:
        return 'Incorrect username / password !'

    msg = "Request Reject "
    sendmsg(mailid, msg)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where HCName ='" + session['hname'] + "' And Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requesttb where HCName ='" + session['hname'] + "' And Status !='waiting' ")
    data1 = cur.fetchall()

    return render_template('HAccept.html', data=data, data1=data1)




@app.route("/ViewImage")
def ViewImage():
    id = request.args.get('id')

    session["rhcid"] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM requesttb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        status = data[8]

    else:
        return 'Incorrect username / password !'
    if status == "Approved":
        return render_template('HDecrypt.html')

    else:
        flash('Your Request Ins Rejected!')
        return render_template('HStatus.html')



@app.route("/imdecrypt", methods=['GET', 'POST'])
def imdecrypt():
    if request.method == 'POST':
        prikey = request.form['prikey']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM requesttb where  id='" + session["rhcid"] + "'")
        data = cursor.fetchone()

        if data:
            imid = data[5]
            tpriKey = data[6]

        else:
            return 'Incorrect username / password !'

        if prikey == tpriKey:

            filepath1 = "./static/Encrypt/" + imid + "_01.png"
            filepath2 = "./static/Encrypt/" + imid + "_02.png"
            filepath3 = "./static/Encrypt/" + imid + "_03.png"
            filepath4 = "./static/Encrypt/" + imid + "_04.png"

            newfilepath1 = "./static/Decrypt/" + imid + "_01.png"
            newfilepath2 = "./static/Decrypt/" + imid + "_02.png"
            newfilepath3 = "./static/Decrypt/" + imid + "_03.png"
            newfilepath4 = "./static/Decrypt/" + imid + "_04.png"

            data1 = 0
            data2 = 0
            data3 = 0
            data4 = 0

            privhex = tpriKey

            with open(filepath1, "rb") as File:
                data1 = base64.b64decode(File.read())

            decrypted_secp = decrypt(privhex, data1)

            with open(newfilepath1, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            with open(filepath2, "rb") as File:
                data2 = base64.b64decode(File.read())

            decrypted_secp = decrypt(privhex, data2)

            with open(newfilepath2, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            with open(filepath3, "rb") as File:
                data3 = base64.b64decode(File.read())
            decrypted_secp = decrypt(privhex, data3)
            with open(newfilepath3, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            with open(filepath4, "rb") as File:
                data4 = base64.b64decode(File.read())
            decrypted_secp = decrypt(privhex, data4)
            with open(newfilepath4, "wb") as DFile:
                DFile.write(base64.b64decode(decrypted_secp))

            flash('Decrypt Successfully all images')
            return render_template('Hmerge.html', sname=imid)



        else:

            flash('Your private key  Incorrect!')
            return render_template('HDecrypt.html')





@app.route("/mergeim", methods=['GET', 'POST'])
def mergeim():
    if request.method == 'POST':
        from PIL import Image
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1vsecureobjectdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM requesttb where  id='" + session["rhcid"] + "'")
        data = cursor.fetchone()

        if data:
            imid = data[5]

        else:
            return 'Incorrect username / password !'

        files = [
            "./static/Decrypt/" + imid + "_01.png",
            "./static/Decrypt/" + imid + "_02.png",
            "./static/Decrypt/" + imid + "_03.png",
            "./static/Decrypt/" + imid + "_04.png"]

        result = Image.new("RGB", (400, 400))

        for index, file in enumerate(files):
            path = os.path.expanduser(file)
            img = Image.open(path)
            img.thumbnail((200, 200), Image.ANTIALIAS)
            x = index // 2 * 200
            y = index % 2 * 200
            w, h = img.size
            print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
            result.paste(img, (x, y, x + w, y + h))

        result.save(os.path.expanduser('static/merge/'+ imid +'.png'))
        from stegano import lsb
        clear_message = lsb.reveal('static/merge/'+ imid +'.png')

        mimage = 'static/merge/'+ imid +'.png'
        session['mimage'] = mimage

        print(clear_message)
        return render_template('HDView.html', iname=mimage, pre=clear_message)




@app.route("/hvdown", methods=['GET', 'POST'])
def hvdown():
    if request.method == 'POST':

        return send_file(session['mimage'], as_attachment=True)

def sendmsg(Mailid,message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
