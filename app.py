import mariadb as db
import os as linux
import sys 
from time import  sleep 
from flask import Flask,render_template,request

# Connect to the database    
conn = None

# Create a cursor object
cursor = None
username = None
password = None
# methods

users = {
    'username' : 'root''keshav''ritika''ANS''amit',
    'pwssd' : 'kr''ANS''ritika''keshav''amit',
} 
    
def insert_into(name,reg,roll,session,branch,year):
    try :
        cursor.execute(f"insert into student_management values('{name}',{reg},{roll},'{session}','{branch}','{year}');")
        print('Query OK ')
        conn.commit() 
        
    except Exception as e:
        print(e)
        return

def isempty(argument):
    if argument:
        return argument
    else :
        return 0
    
app = Flask(__name__)
@app.route('/')


@app.route('/home')
def home():
    return render_template('login.html')       
  
@app.route('/back_home',methods = ["POST",'GET'])
def back_home():
    return render_template('index.html',argument = "_NO OUTPUT_")       

@app.route('/login',methods = ["POST",'GET'])
def logout():
    return render_template('login.html')   

@app.route('/LinuxTerminal',methods = ["POST",'GET'])   
def LinuxTerminal ():
    output = request.form.to_dict()
    cmd = output["Linux"]
    linux.system(command=cmd)
    return render_template('index.html')
  
@app.route('/Signin',methods = ["POST",'GET'])
def Signin():
    
    global conn,cursor,users,username,password
      
    output = request.form.to_dict()
    username = user_input = output["Username"]
    password = pwsd_input = output["password"]
    
    if user_input in users.get('username') and pwsd_input in users.get('pwssd'):
        #update user/password as per your system.
        conn = db.connect(host='localhost', user='root', password='root',database='project')
        cursor = conn.cursor()
        # print('check conn - ' ,bool(conn))

        # return render_template('index.html')
        return render_template('lodingpage.html')
        
    else :
        return render_template('login.html',Error = "username pwsd not found")
    
@app.route('/Loding',methods = ['POST',"GET"])
def Loding():
    global conn,cursor,users,username,password
    
    if username in users.get('username') and password in users.get('pwssd'):
        conn = db.connect(host='localhost', user='root', password='kr',database='project')
        cursor = conn.cursor()
        # print('check conn - ' ,bool(conn))

        return render_template('index.html')
        
    else :
        return render_template('login.html',Error = "username pwsd not found")


@app.route('/inserted_KESHAV_PROJECT',methods = ['POST',"GET"])
def inserted_KESHAV_PROJECT():
    try : 
        output = request.form.to_dict()
        name = output["name"]
        regno = output["regno"]
        rollno = output['rollno']
        
        try:
            regno = int(regno)
            rollno = int(rollno)
        except Exception as e:
            return render_template('index.html',Error= e)
        
        session = output['session']
        Branch = output['Branch']
        year = output['year']
        
        if session :
            pass
        else:
            session='2021-2024'
        if Branch :
            pass
        else:
            Branch='BCA'
        
        insert_into(name=name,reg=regno,roll=rollno,session=session,branch=Branch,year=year)     
        return render_template('index.html',argument = 'Inserted')
    except Exception as e:
         return render_template('index.html')

@app.route('/DeleteAll',methods = ['POST',"GET"])
def DeletedAll():
    output = request.form.to_dict()
    PWSD = int(output['PASSWORD'])
    
    if PWSD == 246890:   
        try:
            cursor.execute("truncate table student_management;")
            print('All records deleted')
            conn.commit()
            return render_template('index.html',argument = 'All record Deleted')
        except Exception as e:
            return render_template('index.html')
    else:
        return render_template('index.html',argument = 'Pwsd error')

@app.route('/DeleteOne',methods = ['POST',"GET"])
def DeleteOne():
    try :
        output = request.form.to_dict()
        keyword = int(output['regstudent'])
        cursor.execute(f"select reg from student_management where reg = {keyword} ;")
        results = cursor.fetchall()
        if bool(results):
            try :
                cursor.execute(f"delete from student_management where reg = {keyword} ;")
                conn.commit()
                return render_template('index.html',argument = f'Reg.no {keyword} Record Deleted')
            except :
                return render_template('index.html',Error= 'error')    
        else:
            return render_template('index.html',argument = "Not valid Reg. no.")     
    except :
        return render_template('index.html')

@app.route('/SearchResult',methods = ['POST',"GET"])
def  SearchResult():
    try:
      output = request.form.to_dict()
      keyword = str(output['detail'])
      cursor.execute("select * from student_management;")
      results = cursor.fetchall()
      text  = []
      for row in results:
        if keyword in str(row):
          text.append(row)
      conn.commit()
      
      string ="\n".join(str(item) for item in text)   
      string =  string.replace('Decimal',' ')
      string =  string.replace(',',' -> ')
      string =  string.replace('(','')
      string =  string.replace(')','')
      string =  " --> Name --> Reg.no. -->  Roll  -->  Session -->  Branch -->  Year <--\n\n"+string
    #   print(string)

      return render_template('index.html',argument = string)
    except Exception as e:
        return render_template('index.html')

@app.route('/Query',methods = ['POST',"GET"])
def Query():
    try:
        output = request.form.to_dict()
        Query_input = str(output['querybox'])
        try :
            cursor.execute(f'{Query_input}' + ';')
            results = cursor.fetchall()
            print(results)
            print('Query ok')
            conn.commit()
        except db.ProgrammingError as e:
            print(str(e))
            return render_template('index.html')
            
        return render_template('index.html',argument = results)
    except Exception as e:
        return render_template('index.html')

@app.route('/Show_record',methods = ['POST','GET'])
def Show_record():
    try:
      cursor.execute('select * from student_management;')

      result = cursor.fetchall()
      text  = []
      count =1
      for row in result:
         text.append(f"{count}>{row}.")
         count+=1
         
      conn.commit()
      # for item in text:
      #   print(item)
      if len(text) == 0:
        e= 'Table empty no records found.'
        return render_template('index.html',Error= e)
        
      string ="\n".join(str(item) for item in text)
      string =  string.replace('Decimal',' ')
      string =  string.replace(',',' -> ')
      string =  string.replace('(','')
      string =  string.replace(')','')
      string =  " --> Name --> Reg.no. -->  Roll  -->  Session -->  Branch -->  Year <--\n\n"+string
    #   print(string) 
    
      return render_template('index.html',argument = str(string))
    except Exception as e:
        return render_template('index.html')

@app.route('/Modify',methods = ['POST','GET'])
def Modify():
    
    output = request.form.to_dict()
    option = output['option']
    option =int(option)
    regno = output['update_reg']
    details = output['update_details'] 
    print(f"while reg str to int  {regno} {details} {option}")
    try: 
        regno = int(regno)
    except Exception as e:
        return render_template('index.html',Error= f"while reg str to int {regno} {details} {option}")
    
    
    if option == (1):      
        cursor.execute(f"update student_management set name = '{details}' where reg = {regno};")
        conn.commit()
        return render_template('index.html',argument= "Name updated.")
        pass
    
    elif option == (2):
        try:
            details = int(details)
            cursor.execute(f"update student_management set roll = {details} where reg = {regno};")
            conn.commit()
            return render_template('index.html',argument= "Roll updated.")
        except Exception as e:
            return render_template('index.html',Error= "while roll str to int ")
        
    elif option == (3):
        
        cursor.execute(f"update student_management set session = '{details}' where reg = {regno};")
        conn.commit()
        return render_template('index.html',argument= "session updated.")
        
        
    elif option == (4):
        year = output['update_details']
        
        if '1' in year or '1st' in year or 'fi' in year or 'Fi' in year or 'first' in year:
            year = '1st-year'
        elif '2' in year or '2nd' in year or 's' in year or 'S' in year or 'second' in year:
            year = '2nd-year'
        elif '3' in year or '3rd' in year or 'ird' in year or 'ird' in year or 'third' in year:
            year = '3rd-year'
        elif '4' in year or '4th' in year or 'fo' in year or 'Fo' in year or 'fourth' in year:
            year = '4th-year'
        else :
            return render_template('index.html',Error= "Not a valid year")
     
        cursor.execute(f"update student_management set year = '{year}' where reg = {regno};")
        conn.commit()
        return render_template('index.html',argument= "Year updated.")
    
    return render_template('index.html',argument= "no update.")

@app.route('/Clear',methods = ['POST','GET'])
def Clear():
    try:
        return render_template('index.html',argument ="")
    except Exception as e:
        return render_template('index.html')

if __name__=='__main__':
    try:
       
        app.run(debug=True,port=8080)
        conn.close()
    except Exception as e:
        exit(0)